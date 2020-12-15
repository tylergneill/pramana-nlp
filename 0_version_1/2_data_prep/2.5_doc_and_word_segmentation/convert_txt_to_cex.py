#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import re
import subprocess

import edit
import resandhify
import validate


resize_only = False
if "--resize_only" in sys.argv: resize_only = True

class Section(object):

	def __init__(self):
		self.section_identifer = ''
		self.doc_identifers = []
		self.doc_contents = []

	def initialize_doc_identifers(self):
		self.doc_identifers = edit.initialize_doc_identifers(
			self.section_identifer, self.doc_identifers)

	def preclean(self):
		for i in range(len(self.doc_contents)):
			regex_replace = [
			# delete (...), punctuation adjacent to numbers, numbers, quotation marksr, extra spacing
			['\([^\)]*?\)', ''],
			['([\|/])+([\d\.,– ]+)(\\1)+', '\\1'],
			['[\d"\t]', ''],
			[' {2,}', ' '],
			# simplify multiple punctuation (also with intervening spaces)
			['([\|/\.] ?)+', '\\1'],
			# space out punctuation as necessary
			[u'([^ ])([\|/\.,;:—\?])', '\\1 \\2'],
			[u'([\|/\.,;:—\?])([^ ])', '\\1 \\2'],
			# carry out manually suggested segmentation
			['_', ' '],
			]
			for r_r in regex_replace: self.doc_contents[i] = re.sub(r_r[0], r_r[1], self.doc_contents[i])

	def resize_docs(self):
		
		self.doc_contents, self.doc_identifers = edit.resize(
			self.doc_contents, self.doc_identifers)



input_path = 'data/input/'
output_path = 'data/output/'

fns = os.listdir(input_path)
fns.sort()
for fn in fns:

	if fn in ['.DS_Store']: continue
	
	full_input_path = os.path.join(input_path, fn)
	
	# validate document structure and content
# 	print "validating structure: %s..." % fn
# 	validation_result = validate.validate_structure(full_input_path, verbose=False)
# 	if validation_result == 0: print "structure of %s does NOT validate, skipping..." % fn; continue
# 	else: print "structure validated, proceeding..."
# 	print "validating content: %s..." % fn
# 	validation_result = validate.validate_content(full_input_path, verbose=False)
# 	if validation_result == 0: print "content of %s does NOT validate, skipping..." % fn; continue
# 	else: print "content validated, proceeding..."
	
	f = open(full_input_path,'r')
	content = f.read().decode('utf-8') # NB!

	print "precleaning and parsing %s..." % fn

	# structural cleaning
	regex_replace = [
	['\n', ''],
	['<[^>]*?>', ''], # get rid of deletable structural info
	['(.){','\\1\n{'], # give non-file-initial {...} sections their own newlines
	]
	for r_r in regex_replace: content = re.sub(r_r[0], r_r[1], content)
	
	sections = content.split('\n') # divide content into {...} sections

	allSections = [] # will collect all Section objects
	all_doc_contents = [] # will isolate all doc content for segmentation and cleaning

	for section in sections:			

		section = re.sub('(\[[^\]]*?\])','\n\\1\n', section) # prepare to divide at identifiers
		subunits = section.split('\n') # divide {...} section into [...]... document-identifier pairs

		S = Section()
		S.section_identifer = subunits[0]	# store {...} section identifier
		S.doc_identifers = subunits[1::2]	# store [...] document identifiers
		S.doc_contents = subunits[2::2]		# store all content
		S.initialize_doc_identifers()		# populate empty []s with counters, etc.

		allSections.append(S)
		for doc_content in S.doc_contents:
			all_doc_contents.append(doc_content)

	# for debugging or illustration
	f_out = open('temp/temp0_original_sections.txt','w')
	f_out.write('\n'.join(all_doc_contents).encode('utf-8'))
	f_out.close()

	print "resizing %s..." % fn

	# compare with final number to get measure of resizing activity
	print "starting number of docs:", len(all_doc_contents)

	# now resize doc_contents, first restricted to sections

	megaS = Section() # will collect all adjusted documents and their identifiers

	for S in allSections:

		S.preclean()
		S.resize_docs()

		for s_m, s_c in zip(S.doc_identifers, S.doc_contents):
			megaS.doc_identifers.append(s_m)
			megaS.doc_contents.append(s_c)

	# do one final resize over all docs

 	megaS.resize_docs()
	# of debatable value, cp. e.g. VS 4,2 and 5,1 combined with each other based on size, despite 4,1 and 5,2

	print "number of resized docs:", len(megaS.doc_contents)

# 	log_file = open('identifier_log.txt','r')
# 	log_content = log_file.read()
# 	log_content = log_content.replace('DEBUG:root:','')
# 	log_file.close()
# 	log_file = open('identifier_log.txt','w')
# 	log_file.write(log_content)
# 	log_file.close()
# 	continue

	# for debugging or illustration
	f_out = open('temp/temp1_resized_documents.txt','w')
 	f_out.write('\n'.join(megaS.doc_contents).encode('utf-8'))
	f_out.close()

	# now clean up and segment all doc_contents at once
	# '#' marks doc boundaries to restore afterward

	if resize_only: 
		# save this file's results to a corresponding two-column tsv file
		f_out = open(os.path.join(output_path, fn),'w')
		for (doc_identifer, doc_content) in zip(megaS.doc_identifers, megaS.doc_contents):
			f_out.write(doc_identifer.encode('utf-8') + '\t' + doc_content.encode('utf-8') + '\n')
		f_out.close()
		continue

	print "segmenting %s..." % fn

	presegmentation_contents = '\n#\n'.join(megaS.doc_contents)

	if fn in resandhify.to_do_list:
		print 'resandhifying....'
		presegmentation_contents = resandhify.resandhify(presegmentation_contents)

	# any remaining '-' must have been intentionally placed by me for segmentation
	presegmentation_contents = presegmentation_contents.replace('-', ' ')

	regex_replace = [
	# use punctuation for more newlines
	[u'([\|/\.,;:—\?] )', '\\1\n'],
	# but not too many
	[u'\n{2,}', '\n'],
	]

	for r_r in regex_replace:
		presegmentation_contents = re.sub(r_r[0], r_r[1], presegmentation_contents)

	# add further newlines to break up lines longer than 128 chars

	lines = presegmentation_contents.split('\n')

	lines2 = []
	for line in lines:
		# all cases >128 must have already been handled manually during cleaning ('_')
		# thus guarantees that split_unit() will work on first try

		try:
			split_up_pieces = edit.split_unit(line, splitpoint_regexes = [u"[' ']"], max_len = 128)
		except RuntimeError:
			import pdb;pdb.set_trace()
			split_up_pieces = edit.split_unit(line, splitpoint_regexes = [u"[' ']"], max_len = 128)
		for l in split_up_pieces:
			lines2.append(l)

	print "number of lines for segmentation:", len(lines2)

	presegmentation_contents = '\n'.join(lines2)

	# now, in order to do e.g. "from sanskrit import apply", would have to convert everything to python3
	# instead, communicate with modified python3 'apply' file via external file i/o and subprocess
	f_out = open('temp/temp2_resized_for_segmenter.txt','w')
	f_out.write(presegmentation_contents.encode('utf-8'))
	f_out.close()

	# raw_input("WAITING FOR HOOMAN") # here is where one can observe, by removing quotation '...', how important apostrophe is for segmentation (e.g. BSJ first section 'praṇamya')

	os.chdir('segmenter')
 	subprocess.call('python3 -W ignore apply.py ../temp/temp2_resized_for_segmenter.txt ../temp/temp3_segmented.txt', shell='True')
	# '-W ignore' for supppressing warning in Terminal
	os.chdir('..')

	# pick results back up
	f_in = open('temp/temp3_segmented.txt','r')
	postsegmentation_contents = (f_in.read()[:-1]).decode('utf-8')
		# delete spurious final newline added by segmenter
	f_in.close()

	# finish clean-up by removing newlines and punctuation, and replacing hyphen with space

	regex_replace = [
	[u'[\n]', ' '],
	[u'[\|/\.,;:—ḷ]', ''], # NB: segmenter turns ? to ḷ via internal transliteration scheme
	['-', ' '], # hyphen, vs em-dash above
	['  ', ' '],
	]
	for r_r in regex_replace:
		postsegmentation_contents = re.sub(r_r[0], r_r[1], postsegmentation_contents)

	# compare with starting number to get measure of resizing activity
	print "final number of docs:", len(postsegmentation_contents.split('#'))

	# count tokens
	num_tokens = postsegmentation_contents.count(' ') - postsegmentation_contents.count('#')
	print "final number of tokens:", num_tokens

	# reincorporate treated content back into master Section object
	megaS.doc_contents = postsegmentation_contents.split('#')

	# for debugging or illustration
	f_out = open('temp/temp4_cleaned.txt','w')
 	f_out.write('\n'.join(megaS.doc_contents).encode('utf-8'))
	f_out.close()

	# convert doc_identifers to CTS URNS
	# TO-DO...

	# save this file's results to a corresponding two-column tsv file
	f_out = open(os.path.join(output_path, fn),'w')
	for (doc_identifer, doc_content) in zip(megaS.doc_identifers, megaS.doc_contents):
		f_out.write(doc_identifer.encode('utf-8') + '\t' + doc_content.encode('utf-8') + '\n')
	f_out.close()

	# ALTERNATIVELY: could here contribute this file's info to a central CTS file
	# TO-DO...

# audibly celebrate finished processing of all files
import time; time.sleep(1); subprocess.call("afplay segmenter/yaas3.mp3", shell='True')