#!/usr/bin/env python
# -*- coding: utf-8 -*-

## adjusts phi values for lambda relevance L and filters unwanted words, considers top max_consider words for each topic and outputs as many as max_show

from collections import Counter, OrderedDict
from tqdm import tqdm
from math import log

L = 0.8

unwanted_words = ['a', 'sva', 'tvam', 'tathā', 'syāt', 'evam', 'āha', 'tva', 'tatra', 'asti', 'yadi', 'kim', 'tasya', 'yathā', 'sa', 'ced', 'yat', 'atas', 'etat', 'katham', 'ayam', 'bhavati', 'atra', 'tasmāt', 'vat', 'tā', 'uktam', 'tatas', 'atha', 'tvena', 'tve', 'asya', 'nanu', 'punar', 'idam', 'tadā', 'ucyate', 'tena', 'tayā', 'tāvat', 'yaḥ', 'sati', 'saḥ', 'sā', 'ādeḥ', 'tarhi', 'ādīnām', 'iva', 'ityādi', 'anena', 'ādayaḥ', 'kutas', 'yatas', 'te', 'iha', 'kaḥ', 'asau', 'kvacid', 'ādau', 'teṣām', 'yatra', 'kaścid', 'yena', 'ādiṣu', 'yasya', 'yadā', 'iyam', 'ukta', 'khalu', 'tām', 'tvasya', 'kiñcid', 'ādikam', 'astu', 'bhavet', 'eṣa', 'ete', 'kintu', 'tam', 'tayoḥ', 'yasmāt', 'ye']

max_consider = 60
max_show = 45

print "preparing phi data...",

try:
	raw_lines = open('phi.csv','r').readlines()
except:
	print "didn't find phi.csv, exiting..."
	exit(0)

split_lines = []
for l in raw_lines:
	split_lines.append(l.split(','))
topic_labels = split_lines[0][1:]
phi_table_lexicon_words = []
for l in split_lines[1:]:
	phi_table_lexicon_words.append(l[0].replace('"',''))
phi_data = [s_l[1:] for s_l in split_lines[1:]]

print "done"

print "preparing lexicon...",

try:
	corpus_tokens = open('corpus_content_only.txt','r').read().replace('\n',' ').replace('=',' ').split(' ')
except:
	print "didn't find corpus_content_only.txt, exiting..."
	exit(0)

num_tokens = len(corpus_tokens)
token_freq_tmp = {}
token_freq = {}
for key, value in Counter(corpus_tokens).items(): token_freq_tmp[key]=value
for key in phi_table_lexicon_words: token_freq[key] = token_freq_tmp[key]		
def prob(w): return (1.0 * token_freq[w] / num_tokens)

print "done"

print "loading and sorting topic information..."

class Topic:
	def __init__(self):
		self.num = 0
		self.label = "" # top_7_words
		self.word_to_phi_adjusted = OrderedDict()
		self.top_words = [] 
Ts = []
for i, label in enumerate(tqdm(topic_labels)):
	T = Topic()
	T.num = i + 1
	T.label = label
	for j, phi_line in enumerate(phi_data):
		word = phi_table_lexicon_words[j].replace('"','')
		phi = float(phi_line[i])  # prob(word | topic)
		phi_adjusted = (L) * log(phi) + (1 - L) * log(phi / prob(word))
		T.word_to_phi_adjusted[word] = phi_adjusted
		# adjusted for relevance
	sorted_d = sorted(T.word_to_phi_adjusted.items(), key=lambda x: -x[1])
# 	import pdb; pdb.set_trace()
	for i in range(max_consider):
		T.top_words.append(sorted_d[:max_consider][i][0].replace('"',''))
	Ts.append(T)

print "done"

print "filtering...",

content_only_top_word_lists = []
for T in Ts:
	content_only_top_word_list = T.top_words
	for u_w in unwanted_words:	
		if u_w in content_only_top_word_list:
			content_only_top_word_list.remove(u_w)
	content_only_top_word_lists.append(content_only_top_word_list[:max_show])

print "done"

print "saving...",

out_buff = ""
for i, tops in enumerate(content_only_top_word_lists):
	out_buff = out_buff + str(i + 1) + '\t' + str(len(tops)) + '\t' + ' '.join(tops) + '\n'
f_out = open('top_words_%d_%d_%.1f.txt' % (max_consider, max_show, L), 'w')
f_out.write(out_buff)
f_out.close()

print "done"