import json
from itertools import izip

import mentiondetection
from meshrecord import MeshRecord


def main():
    mention_result_file = 'e:/el/tmpres/NER/NER/output/00000001.txt'
    merged_result_list = mentiondetection.clean_ner_result(mention_result_file)
    for val in merged_result_list:
        print val.span, val.mtype

    # text_file = 'e:/el/tmpres/NER/NER/00000001.txt.bak'
    # json_result_file = 'e:/el/tmpres/demo/result/result.json'
    #
    # fin = open(text_file, 'rb')
    # text = fin.read().decode('utf-8')
    # fin.close()
    #
    # fin = open(json_result_file, 'rb')
    # # print fin.readline()
    # json_result = json.loads(fin.read())
    # fin.close()
    # mesh_mention_dict = dict()
    # entiies_dict = json_result['entities']
    # spans_list = json_result['spans']
    # idx_list = json_result['idx']
    # for idx, span in izip(idx_list, spans_list):
    #     cur_entity = entiies_dict[str(idx)]
    #     mesh_id = cur_entity.get('mesh-id', '')
    #     if mesh_id:
    #         print idx, span, mesh_id, text[span[0]:span[1] + 1]

if __name__ == '__main__':
    main()
