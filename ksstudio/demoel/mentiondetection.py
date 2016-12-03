from mention import Mention


def span_exist(cur_span, span_list):
    for sp in span_list:
        if not ((cur_span[1] < sp[0]) or cur_span[0] > sp[1]):
            return True
    return False


def clean_ner_result(result_file):
    ord_mention_list = list()
    med_mention_list = list()

    fin = open(result_file, 'rb')
    for line in fin:
        line = line.strip()
        if len(line) == 0:
            continue

        vals = line.strip().split('\t')
        span = (int(vals[0]), int(vals[1]))
        mention = Mention()
        mention.span = span
        if len(vals) == 4:
            mention.mtype = vals[3]
            ord_mention_list.append(mention)
        else:
            mention.mtype = vals[3]
            if vals[4].startswith('MESH'):
                mention.mesh_id = vals[4][5:]
            elif vals[4].startswith('CHEBI'):
                mention.chebi_id = int(vals[4][6:])
            med_mention_list.append(mention)
    fin.close()

    merged_mention_list = list()
    Mention.merge_mention_list(med_mention_list, merged_mention_list)
    Mention.merge_mention_list(ord_mention_list, merged_mention_list)

    return merged_mention_list

    # ord_mention_dict = dict()
    # che_mention_dict = dict()
    # disease_mention_dict = dict()
    #
    # fin = open(result_file, 'rb')
    # for line in fin:
    #     line = line.strip()
    #     if len(line) == 0:
    #         continue
    #
    #     vals = line.strip().split('\t')
    #     span = (int(vals[0]), int(vals[1]))
    #     if len(vals) == 4:
    #         ord_mention_dict[span] = (vals[2], vals[3])
    #     elif vals[3] == 'Chemical':
    #         che_mention_dict[span] = (vals[2], vals[3], vals[4])
    #     elif vals[3] == 'Disease':
    #         disease_mention_dict[span] = (vals[2], vals[3], vals[4])
    # fin.close()
    #
    # merged_result_list = list()
    # che_span_list = che_mention_dict.keys()
    # disease_span_list = disease_mention_dict.keys()
    # for ord_span, tup in ord_mention_dict.iteritems():
    #     if (not span_exist(ord_span, che_span_list)) and (not span_exist(ord_span, disease_span_list)):
    #         merged_result_list.append((ord_span, tup))
    # for che_span, tup in che_mention_dict.iteritems():
    #     if not span_exist(che_span, disease_mention_dict.keys()):
    #         merged_result_list.append((che_span, tup))
    # for disease_span, tup in disease_mention_dict.iteritems():
    #     merged_result_list.append((disease_span, tup))
    #
    # return merged_result_list
