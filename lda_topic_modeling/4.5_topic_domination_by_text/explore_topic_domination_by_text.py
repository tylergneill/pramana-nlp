#!/usr/bin/env python
# -*- coding: utf-8 -*-

## considers top n documents for each of k topics, parses identifiers to reveal which texts dominate that topic

import requests
import re
from collections import Counter
from tqdm import tqdm

n = 1000
k = 75
url = "http://localhost:3737/topic/%s/%s"
topic_search_terms = [str(x+1) for x in range(k)]
doc_search_depth = str(n)

regex_replacements = [
[u'^[a-zāīūṛṝḷṅñṭḍṇśṣḥṃ].*$',''],
[r'^[RT].*$',''],
[r'_.*$',''],
[r'\n{2,}','\n'],
[r'\A\s*', ''],
[r'\s*\Z', '']
]

out_buff = ""
for topic_search_term in tqdm(topic_search_terms):
	r = requests.get(url % (topic_search_term, doc_search_depth) )
	text = r.text
	for r_r in regex_replacements: text = re.sub(r_r[0], r_r[1], text, flags=re.MULTILINE)
	ids = text.split('\n')
	counts = {}
	for key, value in Counter(ids).items(): counts[key] = value
	sorted_counts = sorted(counts.items(), key=lambda x: -x[1])
	out_buff = out_buff + "Topic: %s\n" % topic_search_term
	for i in sorted_counts: out_buff = out_buff + i[0] + ' ' + str(i[1]) + '\n'
	out_buff = out_buff + '\n'
f_out = open('topics_by_text_%s_%s.txt' % (str(n), str(k)),'w')
f_out.write(out_buff.encode('utf-8'))
f_out.close()
