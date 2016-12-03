import math


def find_sentence_ends(tokenized_words):
    sentence_ends = list()
    idx = 0
    num_words = len(tokenized_words)
    while idx < num_words:
        if idx == num_words - 1:
            sentence_ends.append(idx)
        elif tokenized_words[idx] == '.' and len(
                tokenized_words[idx + 1]) > 0 and tokenized_words[idx + 1][0] != '"':
            sentence_ends.append(idx)
        idx += 1
    return sentence_ends


def tokenized_text_match(src_text, tokenized_words):
    pos_list = list()
    cur_pos = 0
    prev_word = ''
    for idx, word in enumerate(tokenized_words):
        hit_pos = cur_pos
        if not word.startswith('formula_') and len(word) > 0:
            if word == '.'and hit_pos > 0:
                hit_pos -= 1
            while hit_pos < len(src_text) and not src_text[hit_pos:].startswith(word):
                hit_pos += 1
            if hit_pos == len(src_text):
                print '%s not found %d' % (word, idx)
                print tokenized_words
            cur_pos = hit_pos + len(word)
        pos_list.append(hit_pos)
        prev_word = word
    return pos_list


def gen_idf_file(text_file, dst_idf_file):
    word_cnt_dict = dict()
    fin = open(text_file, 'rb')
    doc_idx = 0
    for doc_idx, line in enumerate(fin):
        words = line.strip().split(' ')
        doc_words_set = set()
        for word in words:
            if len(word) > 0:
                word = word.lower()
                doc_words_set.add(word)

        for word in doc_words_set:
            word_cnt = word_cnt_dict.get(word, 0)
            word_cnt_dict[word] = word_cnt + 1
    fin.close()

    doc_cnt = float(doc_idx + 1)
    fout = open(dst_idf_file, 'wb')
    for word, cnt in word_cnt_dict.iteritems():
        fout.write('%s\t%f\n' % (word, math.log(doc_cnt / cnt)))
    fout.close()


def main():
    text_file = 'e:/el/tmpres/demo/merge/merged_descriptions_tokenized.txt'
    dst_idf_file = 'e:/el/tmpres/demo/merge/word_idf.txt'
    gen_idf_file(text_file, dst_idf_file)

if __name__ == '__main__':
    main()
