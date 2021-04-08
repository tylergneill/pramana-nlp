#!/usr/bin/env python
# -*- coding: utf-8 -*-

## considers closest n documents to query document, prioritizes set of preferred texts, formats
## relies on modified metallo.go

query_id = "NBhū_104,6^1"
n = 50
priority_ranking = [u'PVin', u'PVA', u'NBh', u'NBhū', u'NV', u'PDhS']

import requests
import json
from collections import OrderedDict

class Hit():
	def __init__(self):
		self.id_name = ""
		self.id_location = ""
		self.rank = 0
		self.distance = ""
#		self.topics = []
#		self.text = ""

url = "http://localhost:3737/view/%s/%d/json" % (query_id, n)
response = requests.get(url)
json_data = json.loads(response.text)
hits = json_data['items']
real_hits = hits[1:]

hits_by_text = OrderedDict()

for h in real_hits:
	H = Hit()
	H.id_name = h['id'][:h['id'].find('_')]
	H.id_location = h['id'][h['id'].find('_')+1:]
	H.rank = h['rank']
	H.distance = h['distance']

	if H.id_name not in hits_by_text:
		hits_by_text[H.id_name] = [(H.rank, H.id_location)]
	elif H.id_name in hits_by_text:
		hits_by_text[H.id_name].append( (H.rank, H.id_location) )

prioritized_hits = OrderedDict()

text_rank = {}
for id in priority_ranking:
	if id not in hits_by_text.keys(): continue
	prioritized_hits[id] = hits_by_text[id]
	hits_by_text.pop(id)
	text_rank[id] = len(prioritized_hits)
for k in hits_by_text.keys():
	prioritized_hits[k] = hits_by_text[k]
	hits_by_text.pop(k)
	text_rank[k] = len(prioritized_hits)

output_lines = []
output_lines.append( [ '\t' + '\t'.join( prioritized_hits.keys() ) ] )
for i in range( len(real_hits) ):
 	output_lines.append( [ '\t' for j in range( len(text_rank)+1 ) ] )
 	output_lines[i+1][0] = str(i+1) + '\t'

for j, (id_name, hits) in enumerate(prioritized_hits.items()):
	for rank, id_location in hits:
		output_lines[rank][j+1] = id_location

f_out = open('doc_similarity_table_%s_%d.tsv' % (query_id, n), 'w')
f_out.write( '\n'.join( [''.join(o_l) for o_l in output_lines] ).encode('utf-8') )
f_out.close()
