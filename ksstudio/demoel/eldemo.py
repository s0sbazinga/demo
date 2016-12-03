import os
from meshtree import MeshTree
from meshrecord import MeshRecord
import ioutils
from medlink import MedLink
import mentiondetection

class GlobalMedLink(object):
    def __init__(self, res_dir):
        wiki_wid_file, wiki_title_file = res_dir + 'wid.txt', res_dir + 'title.txt'
        wiki_links_file, wiki_desc_pos_file = res_dir + 'links.txt', res_dir + 'pos.txt'
        wiki_text_file = res_dir + 'text.txt'
        extra_wiki_desc_file = res_dir + 'wiki_extra_sentences.txt'
        extra_parents_file = res_dir + 'extra_parents.txt'
        name_wid_file = res_dir + 'single_candidates_wid_dict.txt'
        record_file = res_dir + 'records_info_with_wiki.txt'
        dict_file = res_dir + 'med_dict_ascii_with_ids_edited.txt'
        tree_number_file = res_dir + 'id_tn.txt'

        wiki_info = ioutils.load_wiki_info(wiki_wid_file, wiki_title_file, wiki_links_file, wiki_desc_pos_file,
                                           wiki_text_file)

        mesh_records = MeshRecord.load_mesh_records(record_file)
        mesh_tree = MeshTree(tree_number_file, mesh_records)

        extra_wiki_desc = ioutils.load_wiki_extra_sentences(extra_wiki_desc_file)


        self.med_link = MedLink(dict_file, name_wid_file, mesh_records, mesh_tree, wiki_info,
                           extra_wiki_desc, extra_parents_file)


# def main():
#     med_link = init_model()
#     input_file = 'e:/el/tmpres/NER/NER/00000001.txt'
#     output_file = 'e:/el/tmpres/demo/result/result.json'

#     mdel_result = med_link.mdel(input_file)
#     fout = open(output_file, 'wb')
#     fout.write(mdel_result)
#     fout.close()

    # mention_result_file = '/media/dhl/Data/el/tmpres/NER/NER/output/00000001.txt'
    # mention_result_file = 'e:/el/tmpres/NER/NER/output/00000001.txt'
    # merged_result_list = mentiondetection.clean_ner_result(mention_result_file)
    #
    # fin = open(input_file, 'rb')
    # doc_text = fin.read()
    # doc_text = doc_text.decode('utf-8')
    # fin.close()
    #
    # fout = open(output_file, 'wb')
    # fout.write(med_link.link_text(doc_text, merged_result_list))
    # fout.close()


def test():
    # mentiondetection.detect('/home/dhl/data/eldemo/00000001.txt.bak')
    print 'detect'


if __name__ == '__main__':
    # main()
    # test()
    pass
