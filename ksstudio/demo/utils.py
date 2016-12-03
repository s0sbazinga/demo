# coding: utf-8
'''
just some util functions
'''
import os
import re
import hashlib
from docx import Document as Word
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def isempty(sent):
	return sent.strip() == ''

def re_text(text):
	text = re.sub(r'\f', r'', text)
	fake_sents = text.split('\n')
	idx = 0
	for sent in fake_sents:
		if not isempty(sent):
			last_sent = sent
			idx += 1
			break
	num_sents = len(fake_sents)
	paras = []
	last_para = last_sent
	while idx < num_sents - 1:
		cur_sent = fake_sents[idx]
		next_sent = fake_sents[idx+1]
		if isempty(last_sent):
			if isempty(next_sent):
				paras.append(last_para)
				last_para = cur_sent
			else:
				last_para += ' ' + cur_sent
		else:
			last_para += cur_sent
		last_sent = cur_sent
		idx += 1
	if not isempty(fake_sents[idx]):
		add = ' '
		if not isempty(last_sent):
			add = ''
		last_para += add + fake_sents[idx]
	paras.append(last_para)
	return '\n\n'.join(paras)


def text_to_pages(text):
	'''
	split raw text into pages, with each pages 32 lines,
	each line with 100 characters(max)
	return a list a tuples, each tuple store page (beg_pos, end_pos)
	'''
	lines_per_page = 32
	line_width = 100
	page_beg_pos = 0
	cur_line_width = 0
	cur_num_lines = 0
	total_len = len(text)
	pages = []
	pos = 0
	while pos < total_len:
		# eating characters
		if text[pos] == '\n':
			cur_line_width = 0
			cur_num_lines += 1
		else:
			cur_line_width += 1
			# check whether reachers a line width
			if cur_line_width >= line_width:
				cur_line_width = 0
				cur_num_lines += 1
		# check whether reaches a page size
		if cur_num_lines >= lines_per_page:
			while text[pos] != ' ':
				pos -= 1
			pages.append((page_beg_pos, pos + 1))
			page_beg_pos = pos + 1
			cur_line_width = 0
			cur_num_lines = 0
		pos += 1
	if page_beg_pos < total_len - 1:
		pages.append((page_beg_pos, total_len))
	return pages


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=0,
  								  password="", caching=True,
  								  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def read_document(file_path, file_ext):
	if file_ext == "docx" or file_ext == "doc":
		doc = Word(docx=file_path)
		doc_text = '\n\n'.join([para.text.encode('utf-8')
			                    for para in doc.paragraphs])
		return doc_text
	elif file_ext == 'pdf':
		return convert_pdf_to_txt(file_path)
	else:
		with open(file_path, 'r') as f:
			doc_text = f.read()
		return doc_text

def gen_salt():
	import random
	import string
	return ''.join([random.choice(string.printable)
		           for i in xrange(10)])

def hash_to_path(root, hash, ext='txt'):
	file_path = 'edl/' + hash +'.' + ext
	return os.path.join(root, file_path)
