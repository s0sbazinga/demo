#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template.context_processors import csrf
from django.contrib import messages
from django.conf import settings

from .models import Document
from .models import EdlRecord

import os
import sys
import re
import json
import time
import random
# import pyjsonrpc

# demoel_module_path = os.path.join(settings.BASE_DIR, 'demoel')
# sys.path.insert(0, demoel_module_path)
# print sys.path
# import eldemo
from .utils import *
from .main import DemoEntityLinking, DemoRelatinDiscovery

media_root = settings.MEDIA_ROOT
# DEMOEL_MODULE_PATH = os.path.join(settings.BASE_DIR, 'demoel')
# DEMOEL_RES_PATH = os.path.join(settings.BASE_DIR, 'demoel/del-data/')
# sys.path.insert(0, DEMOEL_MODULE_PATH)
# from eldemo import GlobalMedLink
# EL_DEMO = GlobalMedLink(DEMOEL_RES_PATH)

# Create your views here.
def index(request):
	response = render(request, 'index.html')
	response['Expires'] = 'Mon, 26 Jul 1997 05:00:00 GMT'
	response['Cache-Control'] = 'no-store, must-revalidate'
	response['Pragma'] = 'no-cache'
	return response

def upload(request):
	mes = messages.get_messages(request)
	err_msg = None
	for m in mes:
		if m.tags == 'error':
			err_msg = m
	context = {}
	if err_msg:
		context = {'err': err_msg}
	return render(request, 'lp.html', context)

def process(request):
	if request.method == 'POST':
		type_dict = {'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
		             'application/msword': 'doc',
		             'application/wps-office.docx': 'docx',
		             'application/wps-office.doc': 'doc',
		             'application/pdf': 'pdf',
		             'text/plain': 'txt'}
		uploaded_file = request.FILES['file_to_label']
		if uploaded_file.size >= 20 * (1024**2):
			messages.error(request, '请上传小于20M的文件!!!')
			return HttpResponseRedirect('/lp')
		filetype = uploaded_file.content_type
		# file_hash = hashlib.md5(gen_salt() + uploaded_file.name).hexdigest()
		file_ext = type_dict.get(filetype, None)
		if not file_ext:
			messages.error(request, '不支持的文件类型!!!')
			return HttpResponseRedirect('/lp')

		uploaded_file_path = uploaded_file.temporary_file_path()
		start_time = time.time()

		# read file
		# uploaded_file_name = uploaded_file.name.split('.')[0]
		# file_path = file_hash + '_' + uploaded_file_name + '.' + file_ext
		# file_path = os.path.join(settings.MEDIA_ROOT, file_path)
		try:
			doc_text = read_document(uploaded_file_path, file_ext)
		except:
			messages.error(request, '文件包含非法字符，读取失败!!!')
			return HttpResponseRedirect('/lp')
		doc_text = re_text(doc_text)

		edl_file_hash = hashlib.md5(gen_salt() + doc_text).hexdigest()
		edl_txt_file = hash_to_path(media_root, edl_file_hash)
		with open(edl_txt_file, 'w+') as f:
			f.write(doc_text.decode('utf-8').encode('utf-8'))

		# old demo soap link: remove TODO
		# new TODO(JSON RPC)
		# soap_client = SoapClient("http://localhost:8187/linkws?wsdl")
		# result = soap_client.service.linkUploadedFile(file_path)

		# http_client = pyjsonrpc.HttpClient(
		# 	url = 'http://10.214.129.201:9090',
		# )
		# # med_link = EL_DEMO.med_link
		# static_input = 'ner/00000001.txt.bak'
		# ner_file_path = 'ner/00000001.txt.ner'
		# http_response = http_client.call('medlink', static_input, ner_file_path)
		# # print http_response
		# result = json.loads(http_response)

		# static_input = os.path.join(settings.BASE_DIR, 'demoel/ner/00000001.txt.bak')
		# static_ner = os.path.join(settings.BASE_DIR, 'demoel/ner/00000001.txt.ner')
		# med_link = settings.EL_DEMO.med_link
		# result = json.loads(med_link.mdel(static_input, static_ner))
		# end = time.clock()
		# print 'time: ', end - start

		# edl_json_file = hash_to_path(media_root, edl_file_hash, 'json')
		# json.dump(result, open(edl_json_file, 'w+'), indent=2)

		# # store record to db
		# edl_record = EdlRecord(original_file=new_file, result_file=edl_file_hash)
		# edl_record.save()

		# from django.core.urlresolvers import reverse
		# print reverse('demo', args=(edl_file_hash,))

		# save file upload record
		end_time = time.time()
		new_file = Document(upfile_hash=edl_file_hash,
			 				upfile_name=uploaded_file.name,
			                upfile_type=file_ext,
			                process_time=end_time-start_time)
		new_file.save()

		return redirect('demo', edl=edl_file_hash)
	else:
		raise Http404()


def demo(request, edl=None):
	# entity linking testing
	edl = 'disease'
	if not edl:
		raise Http404()
	orig_file_path = hash_to_path(media_root, edl)
	edl_file_path = hash_to_path(media_root, edl, 'json')
	sf_file_path = os.path.join(media_root, 'test/sf.json')
	if not os.path.isfile(orig_file_path):
		raise Http404()
	if not os.path.isfile(edl_file_path):
		raise Http404()
	if not os.path.isfile(sf_file_path):
		raise Http404()

	if request.is_ajax():
		page_num = request.GET.get('page', None)
		op = request.GET.get('op', None)
		try:
			page_num = int(page_num)
		except ValueError:
			raise Http404()

		with open(orig_file_path) as f:
			orig_text = f.read().decode('utf-8')

		el_result = json.load(open(edl_file_path))
		pages = text_to_pages(orig_text)

		if page_num > len(pages):
			raise Http404()
		if op not in ['edl', 'sf']:
			raise Http404()

		b, e = pages[page_num - 1]
		if op == 'edl':
			el_result = json.load(open(edl_file_path))
			demo_el = DemoEntityLinking((b, e), orig_text[b: e], el_result)
			demo_text = demo_el.do_demo()
		else:
			test_sf_result = json.load(open(sf_file_path))
			demo_sf = DemoRelatinDiscovery((b, e), orig_text[b: e], test_sf_result)
			demo_text = demo_sf.do_demo()
		# print demo_text
		demo_text = re.sub(r'\n', r'<br/>', demo_text)
		# return render(request, 'highlight.html', {'demo_html': demo_text})
		return HttpResponse(demo_text)
	elif request.method == 'GET':
		# test_output = os.path.join(settings.MEDIA_ROOT, 'test/test-result.json')
		# test_sf_output = os.path.join(settings.MEDIA_ROOT, 'test/test-sf.json')
		# test_result = json.load(open(test_output))
		test_sf_result = json.load(open(sf_file_path))
		with open(orig_file_path) as f:
			orig_text = f.read().decode('utf-8')
		# orig_text = re_text(orig_text)
		el_result = json.load(open(edl_file_path))

		# get stat results
		stat_el = DemoEntityLinking((0, 0), orig_text, el_result)
		statistics = stat_el.do_stat()
		for k, v in statistics.items():
			n, t = v
			g = random.randint(100000, 300000)
			v = 'New: %s<br>Total: %s in %s' % (n, t, g)
			statistics.update({k: v})

		# pagination
		pages = text_to_pages(orig_text)
		start_page = 0
		beg, end = pages[start_page]
		page_text = orig_text[beg: end]
		demo_el = DemoEntityLinking((beg, end), page_text, el_result)
		demo_text = demo_el.do_demo()

		# slot filling test
		# sf_pages = text_to_pages(test_sf_input)
		# sb, se = sf_pages[0]
		# sf_page_text = test_sf_input[sb: se]
		demo_sf = DemoRelatinDiscovery((beg, end), page_text, test_sf_result)
		demo_sf_text = demo_sf.do_demo()
		return render(request, 'edl.html', {'demo_html': demo_text,
											'stat': statistics,
			                                'demo_sf_html': demo_sf_text,
			                                'maxpages': len(pages)})
