'''
some classes
'''

import json
from collections import deque


class DemoEntityLinking(object):
	def __init__(self, span, input=None, result=None):
		self.raw = input
		self.beg, self.end = span
		if result:
			self.entities = result['entities']
			self.entity_idxs = result['idx']
			self.entity_types = result['type']
			self.entity_spans = result['spans']
		self.__bad_entity = -1
		self.statistics = {}

	def decorate_entity(self, html_id, idx, entity_text):
		eidx = self.entity_idxs[idx]
		e_type = self.entity_types[idx].lower()
		html_id = 'e_%d' % html_id

		is_new_entity = self._is_new_entity(idx)
		# if e_type == 'per':
		# 	print 'hehe:', is_new_entity
		# new, total = self.statistics.get(e_type, (0, 0))
		sup = eidx
		if is_new_entity:
			# new += 1
			if eidx == -1:
				sup = ''
			e_class = 'marked_span newe'
		else:
			e_class = 'marked_span olde'
		# total += 1
		# self.statistics.update({e_type: (new, total)})
		decorated_text = '<span id="%s" class="%s et_%s">%s<sup>%s</sup></span>' \
		                 % (html_id, e_class, e_type, entity_text, sup)
		return decorated_text

	def _format_desc(self, desc, name, id, type):
		if not name or not id:
			return ('<span class="%s">%s'
			        '[<b>%s</b>]</span>') % (type.lower(), desc, type)
		return ('<span class="%s">%s'
			    '[<i>%s</i> (%s), <b>%s</b>].  </span>') % (type.lower(), desc, name, id, type)

	def build_entity_infobox(self, html_id, eidx):
		box_id = 'bub_%d' % html_id
		infobox = '<div id="%s" class="bub_div">' % box_id

		# build mesh link
		hint = 'Click to edit.'
		chebi_desc_info = ''
		mesh_desc_info = ''
		wiki_desc_info = ''

		# chebi_syno_info = self._build_list_group([hint])
		# mesh_syno_info = self._build_list_group([hint])
		# wiki_link_info = self._build_list_group([hint])
		chebi_syno_info = ''
		mesh_syno_info = ''
		wiki_link_info = ''

		tree_info = {'mesh': [], 'wiki': []}
		tree_info = json.dumps(tree_info)
		if eidx != self.__bad_entity:
			entity = self.entities[str(eidx)]
			mesh_id = entity.get('mesh-id', None)
			chebi_id = entity.get('chebi-id', None)
			if chebi_id:
				chebi_name = entity['chebi-name']
				chebi_desc = entity['chebi-description']
				chebi_desc_info = self._format_desc(chebi_desc, chebi_name, chebi_id, 'ChEBI')
				chebi_syno_info = self._build_list_group(entity['chebi-synonyms'])

			if mesh_id:
				mesh_name = entity['mesh-name']
				mesh_desc = entity['mesh-description']
				mesh_desc_info =  self._format_desc(mesh_desc, mesh_name, mesh_id, 'MeSH')
				if entity['mesh-synonyms']:
					mesh_syno_info = self._build_list_group(entity['mesh-synonyms'])

				# building tree
				mesh_tn = entity['mesh-tn']
				tree_info = []
				for tn in mesh_tn:
					mesh_parents = entity['mesh-parents'][tn]
					leaf = [[mesh_id, mesh_name, tn]]
					subtree = self._build_tree(leaf, mesh_parents)
					tree_info += subtree
					# leafs.append([mesh_id, mesh_name, tn])
				# entity_node = [[mesh_id, mesh_name, mesh_tn]]
				# tree_info = self._build_tree(leafs, mesh_parents)

				# extra tree information (from wikipedia is-a rule)
				extra_parents = entity.get('extra-parent', [])
				extra_trees = []
				if extra_parents:
					for e_parents in extra_parents:
						if e_parents:
							extra_tree = self._build_tree([], e_parents)
							head = extra_tree[0]['text']
							extra_tree[0].update({'text': head})
							extra_trees += extra_tree
					# tree_info += extra_trees
				tree_info = {'mesh': tree_info, 'wiki': extra_trees}
				tree_info = json.dumps(tree_info)

			# build wikipedia link
			# print eidx
			wiki_id = entity.get('wid', None)
			if wiki_id:
				wiki_title = entity.get('wiki-title', None)
				if wiki_title:
					wiki_url = 'https://en.wikipedia.org/w/index.php?curid=%s' % wiki_id
					wiki_desc = entity.get('wiki-text', None)
					wiki_name = '<a href="%s"><i>%s</i></a>' % (wiki_url, wiki_title)
					wiki_desc_info = self._format_desc(wiki_desc, wiki_name, wiki_id, 'Wikipedia')

					wiki_link_list = []
					for l in entity['wiki-links']:
						s = '_'.join(l.split())
						wiki_link_list.append('https://en.wikipedia.org/wiki/%s' % s)
					wiki_link_info = self._build_list_group(entity['wiki-links'], wiki_link_list)
					# wiki_link_info = '<div id="wiki">%s</div>' % wiki_link_info
			# syno_info = '<div id="mesh">%s</div>' % syno_info

		mesh_syno_info = '<div id="mesh">%s</div>' % mesh_syno_info
		chebi_syno_info = '<div id="chebi">%s</div>' % chebi_syno_info
		wiki_link_info = '<div id="wiki">%s</div>' % wiki_link_info

		all_desc_info = '%s%s%s' % (mesh_desc_info, chebi_desc_info, wiki_desc_info)
		if all_desc_info == '':
			all_desc_info = '<span>Click to edit</span>'
		all_desc_info = ('<div id="edesc"><p class="editable" data-type="textarea">'
						 '%s</p><hr></div>') % (all_desc_info,)
		all_syno_info = '<div id="esyno">%s%s%s</div>' % (mesh_syno_info, chebi_syno_info, wiki_link_info)
		tree_info = '<div id="etree">%s<hr></div>' % tree_info
		infobox += all_desc_info + all_syno_info + tree_info + '</div>'
		return infobox

	def _build_list_group(self, text, link=None):
		links = ''
		for i, t in enumerate(text):
			if not link:
				href = '<li class="list-group-item">%s</li>' % t
			else:
				href = '<a class="list-group-item" href="%s">%s</a>' % (link[i], t)
			links += href
		if not link:
			list_group = '<ul class="list-group">%s</ul>' % links
		else:
			list_group = '<div class="list-group">%s</div>' % links
		return list_group

	def _build_tree(self, leafs, nodes):
		# nodes.append(entity)
		all_nodes = nodes + leafs
		fake_tree = {}
		tree_nodes = {}
		for node in all_nodes:
			fake_tree.update({node[2]: []})
			real_node = {'text': node[1],
						 'href': '#%s (%s)' % (node[2], node[0]),
			             'nodes': [] }
			if node in leafs:
				real_node = {'text': node[1],
				             'href': '#%s (%s)' % (node[2], node[0]),
				             'color': '#D9534F'}
			tree_nodes.update({node[2]: real_node})
		roots = []
		for node in all_nodes:
			steps = node[2].split('.')
			if len(steps) == 1:
				roots.append(node[2])
				continue
			parent_key = '.'.join(steps[0:-1])
			children = fake_tree.get(parent_key, [])
			children.append(node[2])

		leafs = deque()
		for root, children in fake_tree.items():
			if not len(children):
				leafs.append(root)

		while len(leafs):
			leaf = leafs.popleft()
			steps = leaf.split('.')
			if len(steps) == 1:
				continue
			parent_key = '.'.join(steps[0:-1])
			leaf_node = tree_nodes[leaf]
			children = tree_nodes[parent_key]['nodes']
			children.append(leaf_node)
			tree_nodes[parent_key].update({'nodes': children})
			fake_tree[parent_key].remove(leaf)
			if not len(fake_tree[parent_key]):
				leafs.append(parent_key)
		tree_info = []
		for root in roots:
			tree_nodes[root].update({'color': '#489cdf'})
			tree_info.append(tree_nodes[root])
		return tree_info

	def _is_span_inpage(self, w_beg, w_end):
		if w_beg >= self.beg and w_beg < self.end:
			return True
		return False

	def _is_new_entity(self, i):
		if self.entity_idxs[i] == self.__bad_entity:
			return True
		else:
			eidx = str(self.entity_idxs[i])
			mesh_id = self.entities[eidx].get('mesh-id', None)
			chebi_id = self.entities[eidx].get('chebi-id', None)
			has_mesh_link = False
			has_chebi_link = False
			if mesh_id: has_mesh_link = True
			if chebi_id: has_chebi_link = True
			if not has_mesh_link and not has_chebi_link:
				return True
			return False

	def do_stat(self):
		total_len = len(self.entity_idxs)
		for i in xrange(total_len):
			is_new_entity = self._is_new_entity(i)
			e_type = self.entity_types[i].lower()
			new, total = self.statistics.get(e_type, (0, 0))
			if is_new_entity: new += 1
			total += 1
			self.statistics.update({e_type: (new, total)})
		return self.statistics

	def do_demo(self):
		demo_text = ''
		pointer = 0
		html_id = 0
		for i, span in enumerate(self.entity_spans):
			if not self._is_span_inpage(*span):
				continue

			# filter...
			if self.entity_types[i].lower() == 'gpe':
				continue
			# is_new_entity = self._is_new_entity(i)
			entity_beg = span[0] - self.beg
			entity_end = span[1] - self.beg
			demo_text += self.raw[pointer : entity_beg]
			entity_text = self.raw[entity_beg : entity_end + 1]
			# if span[0] == 4120:
			# 	print 'from main:', entity_text
			decorated_text = self.decorate_entity(html_id, i,
				                                  entity_text)
			demo_text += decorated_text
			infobox_text = self.build_entity_infobox(html_id, self.entity_idxs[i])
			if isinstance(infobox_text, str):
				infobox_text = infobox_text.decode('utf-8')
			demo_text += infobox_text
			pointer = entity_end + 1
			html_id += 1
		demo_text += self.raw[pointer:]

		# html_id = 0
		# for eidx, span in zip(self.entity_idxs, self.entity_spans):
		# 	if not self._is_span_inpage(*span):
		# 		continue
		# 	is_new_entity = self._is_new_entity()
		# 	infobox_text = self.build_entity_infobox(html_id, str(eidx))
		# 	# print type(infobox_text)
		# 	demo_text += infobox_text.encode('utf-8')
		# 	html_id += 1
		return demo_text


class DemoRelatinDiscovery(object):
	def __init__(self, span, input=None, result=None):
		self.beg, self.end = span
		self.raw = input
		self.sf_sents = result

	def _is_span_inpage(self, w_beg, w_end):
		if w_beg >= self.beg and w_end < self.end:
			return True
		return False

	def decorate_sent(self, idx, spans, sent_text):
		subj_span, obj_span = spans
		sx, sy = subj_span
		ox, oy = obj_span
		# print subj_span, obj_span
		subj_text = sent_text[sx: sy]
		obj_text = sent_text[ox: oy]
		subj_text = '<span id="subj_%s" class="%s">%s</span>' % (idx, 'marked_subj', subj_text)
		obj_text = '<span id="obj_%s" class="%s">%s</span>' % (idx, 'marked_obj', obj_text)
		if sx < ox:
			demo_sent = sent_text[:sx]
			demo_sent += subj_text + sent_text[sy:ox]
			demo_sent += obj_text + sent_text[oy:]
		else:
			demo_sent = sent_text[:ox]
			demo_sent += subj_text + sent_text[oy:sx]
			demo_sent += obj_text + sent_text[sy:]
		demo_sent = '<span id="sf_sent_%s" class="%s">%s</span>' % (idx, 'marked_sf_sent', demo_sent)
 		return demo_sent

 	def _correct_span(self, span):
 		return (span[0] - self.beg, span[1] - self.beg)

	def do_demo(self):
		demo_sf_text = ''
		pointer = 0
		idx = 0
		for sent in self.sf_sents:
			sent_span = sent['sentences']
			if not self._is_span_inpage(*sent_span):
				continue
			subj_span = self._correct_span(sent['chemical'])
			obj_span = self._correct_span(sent['disease'])
			sent_span = self._correct_span(sent_span)
			b, e = sent_span
			demo_sf_text += self.raw[pointer: b]
			sent_text = self.raw[b: e]
			# print 'hehe:', sent_text
			xs, ys = subj_span
			xo, yo = obj_span
			subj_span = xs - b, ys - b
			obj_span = xo - b, yo - b
			spans = (subj_span, obj_span)
			d_sent_text = self.decorate_sent(idx,
											 spans,
											 sent_text)
			demo_sf_text += d_sent_text
			# sf_infobox_text = self.build_sf_infobox(idx, sent)
			pointer = e
			idx += 1
		demo_sf_text += self.raw[pointer:]
		return demo_sf_text