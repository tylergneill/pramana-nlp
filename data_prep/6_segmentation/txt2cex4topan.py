"""
	Input: Multiple .txt with [...]/{...} document candidates and <...>/(...) notes
	Output: Single .cex with identifiers and modified document contents.

	Algorithm:

		Read in .txt files from data/input

		For each file:

			1) doc_prep

			Remove <...>/(...) notes
			Remove empty [...] identifiers and {...} labels
			Split into {...} sections
			For each {...} section:
				Split into [...] document candidates
				(Log original doc candidate number to data/output/logging/stats.tsv)
				(Log id/content pairs to data/output/logging/0_original_doc_candidates.tsv)
				Resize [...] document candidates and modify identifiers accordingly
			(Log resized doc number to data/output/logging/stats.tsv)
			(Log resized id/content pairs to data/output/logging/1_resized_docs.tsv)

			2) word_split

			Create global newline-separated buffer with all document contents
			Use single SplitterWrapper call to word-split file contents (maintain punctuation)
				Wrapper first splits on all punctuation
				Wrapper also splits again where len > 128
				Internally logs number of lines
				Then does splits
				Finally reassembles with original punctuation
				Returns resulting string and log info
			(Log splititng-lines and words numbers to data/output/logging/stats.tsv)
			(Log word-split id/content pairs to data/output/logging/2_split_words.tsv)

			3) finalize_cex

			Remove punctuation and Splitter symbols
			Extend identifiers according to convention
			Append to .cex block list(s)
			(Log finalized id/content pairs to data/output/logging/3_finalized_lda_docs.tsv)

		Combine and save results to .cex file in data/output/pramana-nlp_TIMESTAMP.cex

"""

import sys
import os.path
import re
import subprocess
# > from skrutable.HellwigNehrdichSplitter import SplitterWrapper

import resize
# import resandhify
# import validate

input_path = 'data/input/'
output_path = 'data/output/'

logging_path_prefix = 'data/output/logging/'
stats_buffer = '\t'.join([
	"filename", "docs_orig", "docs_resized", "seg_lines", "tokens"
	]) + '\n' # header row

class Section(object):

	def __init__(self):
		self.section_label = ''
		self.doc_identifers = []
		self.doc_contents = []

#	# NOT DOING THIS ANYMORE
# 	def initialize_doc_identifers(self):
# 		self.doc_identifers = edit.initialize_doc_identifers(
# 			self.section_label, self.doc_identifers)

	def preclean(self):
		for i in range(len(self.doc_contents)):
			regex_replace = [
			# delete (...), punctuation adjacent to numbers, numbers, quotation marks, extra spacing
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
		# lower bound: resize.min_doc_size
		# upper bound: resize.max_doc_size (also a few cases of min_doc_size + max_doc_size ??)
		temp_content_L, temp_identifier_L = resize.split_big_docs(self.doc_contents, self.doc_identifers)
		self.doc_contents, self.doc_identifers = resize.combine_small_docs(temp_content_L, temp_identifier_L)

fns = os.listdir(input_path)
fns.sort()
for fn in fns:

	if fn in ['.DS_Store']: continue # skip those macOS rascals

	full_input_path = os.path.join(input_path, fn)
	with open(full_input_path, 'r') as f_in:
		f_data = f_in.read()

	print("precleaning and parsing %s..." % fn)

	# structural (=bracket) validation at this point would be smart

	# do some structural cleaning
	regex_replacement = [
		['<[^>]*?>', ''], # discard <...>
		['\([^\)]*?\)', ''], # discard (...)
		['\n', ''], # discard all newlines
		['\[[^\]]*?\]([\[{])', '\\1'], # discard [...] identifiers with no content (repeat!)
		['{[^}]*?}{', '{'], # discard {...} labels with no content (repeat!)
		['(.){','\\1\n{'], # create newline for each (non-file-initial) {...}
	]
	to_repeat = ['\[[^\]]*?\]\[', '\{[^\}]*?\}\{']
	for r_r in regex_replacement:
		f_data = re.sub(r_r[0], r_r[1], f_data)
		if r_r[0] in to_repeat: # repeat as necessary
			while bool( re.match(r_r[0], f_data) ) == True:
				f_data = re.sub(r_r[0], r_r[1], f_data)

	file_sections = f_data.split('\n') # divide into {...} sections

	all_Sections = [] # will collect all resulting Section objects

	all_doc_identifiers = []
	all_doc_contents = [] # will isolate all doc content for segmentation and cleaning

	for section in file_sections:

		section = re.sub('(\[[^\]]*?\])','\n\\1\n', section) # add newlines for following split
		ids_and_contents = section.split('\n') # divide into [...] identifiers and contents

		S = Section()
		S.section_label = ids_and_contents[0]		# store {...} section label
		S.doc_identifers = ids_and_contents[1::2]	# store [...] document identifiers
		S.doc_contents = ids_and_contents[2::2]		# store document contents

		S.doc_count_before_resize = 0
		S.doc_count_after_resize = 0
		S.line_count_for_seg = 0
		S.token_count = 0

		all_Sections.append(S)

		for doc_identifier in S.doc_identifers:
			all_doc_identifiers.append(doc_identifier)
		for doc_content in S.doc_contents:
			all_doc_contents.append(doc_content)

	# log
	logging_path_suffix = '0_original_doc_candidates/'
	full_logging_f_path = os.path.join(logging_path_prefix, logging_path_suffix, fn)
	with open(full_logging_f_path ,'w') as f_out:
		f_out.write('\n'.join(
			[ id + '\t' + c for id, c in zip(all_doc_identifiers, all_doc_contents) ]
			)
		)

	print("resizing %s..." % fn)

	# now resize doc_contents, first restricted to sections

	megaS = Section() # will collect all adjusted documents and their identifiers
	megaS.section_label = fn
	megaS.doc_count_before_resize = len(all_doc_contents)

	for S in all_Sections:

		S.preclean()
		S.resize_docs()

		for s_m, s_c in zip(S.doc_identifers, S.doc_contents):
			megaS.doc_identifers.append(s_m)
			megaS.doc_contents.append(s_c)

	megaS.doc_count_after_resize = len(megaS.doc_contents)

	# log
	logging_path_suffix = '1_resized_docs/'
	full_logging_f_path = os.path.join(logging_path_prefix, logging_path_suffix, fn)
	with open(full_logging_f_path ,'w') as f_out:
		f_out.write('\n'.join(
			[ id + '\t' + c for id, c in zip(megaS.doc_identifers, megaS.doc_contents) ]
			)
		)

#	# NOT DOING THIS ANYMORE
# 	# do one final resize over all docs
#  	megaS.resize_docs()
# 	# of debatable value, cp. e.g. VS 4,2 and 5,1 combined with each other based on size, despite 4,1 and 5,2

	# now clean up and segment all doc_contents at once
	# '#' marks doc boundaries to restore afterward

	print("segmenting %s..." % fn)

	presegmentation_contents = '\n#\n'.join(megaS.doc_contents)

#	# NOT DOING THIS ANYMORE
# 	if fn in resandhify.to_do_list:
# 		print('resandhifying....')
# 		presegmentation_contents = resandhify.resandhify(presegmentation_contents)

	# any remaining '-' must have been intentionally placed by me for segmentation
	presegmentation_contents = presegmentation_contents.replace('-', ' ')

# 	# use punctuation for more newlines
# 	regex_replace = [
# 	[u'([\|/\.,;:—\?] )', '\\1\n'],
# 	# but not too many
# 	[u'\n{2,}', '\n'],
# 	]
#
# 	for r_r in regex_replace:
# 		presegmentation_contents = re.sub(r_r[0], r_r[1], presegmentation_contents)
#
# 	# add further newlines to break up lines longer than 128 chars
#
# 	lines = presegmentation_contents.split('\n')
#
# 	lines2 = []
# 	for line in lines:
# 		# all cases >128 must have already been handled manually during cleaning ('_')
# 		# thus guarantees that split_unit() will work on first try
#
# 		try:
# 			split_up_pieces = edit.split_unit(line, splitpoint_regexes = [u"[' ']"], max_len = 128)
# 		except RuntimeError:
# 			import pdb;pdb.set_trace()
# 			split_up_pieces = edit.split_unit(line, splitpoint_regexes = [u"[' ']"], max_len = 128)
# 		for l in split_up_pieces:
# 			lines2.append(l)
#
# 	print("number of lines for segmentation:", len(lines2))
# S.line_count_for_seg = 0
#
# 	presegmentation_contents = '\n'.join(lines2)
#
# 	# now, in order to do e.g. "from sanskrit import apply", would have to convert everything to python3
# 	# instead, communicate with modified python3 'apply' file via external file i/o and subprocess
# 	f_out = open('temp/temp2_resized_for_segmenter.txt','w')
# 	f_out.write(presegmentation_contents.encode('utf-8'))
# 	f_out.close()
#
# 	# raw_input("WAITING FOR HOOMAN") # here is where one can observe, by removing quotation '...', how important apostrophe is for segmentation (e.g. BSJ first section 'praṇamya')
#
# 	os.chdir('segmenter')
#  	subprocess.call('python3 -W ignore apply.py ../temp/temp2_resized_for_segmenter.txt ../temp/temp3_segmented.txt', shell='True')
# 	# '-W ignore' for supppressing warning in Terminal
# 	os.chdir('..')
#
# 	# pick results back up
# 	f_in = open('temp/temp3_segmented.txt','r')
# 	postsegmentation_contents = (f_in.read()[:-1]).decode('utf-8')
# 		# delete spurious final newline added by segmenter
# 	f_in.close()
#
# 	# finish clean-up by removing newlines and punctuation, and replacing hyphen with space
#
# 	regex_replace = [
# 	[u'[\n]', ' '],
# 	[u'[\|/\.,;:—ḷ]', ''], # NB: segmenter turns ? to ḷ via internal transliteration scheme
# 	['-', ' '], # hyphen, vs em-dash above
# 	['  ', ' '],
# 	]
# 	for r_r in regex_replace:
# 		postsegmentation_contents = re.sub(r_r[0], r_r[1], postsegmentation_contents)
#
# 	# compare with starting number to get measure of resizing activity
# 	print("final number of docs:", len(postsegmentation_contents.split('#')))
#
# 	# count tokens
# 	num_tokens = postsegmentation_contents.count(' ') - postsegmentation_contents.count('#')
# 	print("final number of tokens:", num_tokens)
# S.token_count = 0
# 	# reincorporate treated content back into master Section object
# 	megaS.doc_contents = postsegmentation_contents.split('#')
#
# 	# for debugging or illustration
# 	f_out = open('temp/temp4_cleaned.txt','w')
#  	f_out.write('\n'.join(megaS.doc_contents).encode('utf-8'))
# 	f_out.close()
#
# 	# convert doc_identifers to CTS URNS
# 	# TO-DO...
#
# 	# save this file's results to a corresponding two-column tsv file
# 	f_out = open(os.path.join(output_path, fn),'w')
# 	for (doc_identifer, doc_content) in zip(megaS.doc_identifers, megaS.doc_contents):
# 		f_out.write(doc_identifer.encode('utf-8') + '\t' + doc_content.encode('utf-8') + '\n')
# 	f_out.close()
#
# 	# ALTERNATIVELY: could here contribute this file's info to a central CTS file
# 	# TO-DO...

	stats_buffer += '\t'.join([
		fn,
		str(megaS.doc_count_before_resize),
		str(megaS.doc_count_after_resize),
		"0",
		"0"
		]) + '\n'

# final logging of stats
full_logging_f_path = os.path.join(logging_path_prefix, 'stats.tsv')
with open(full_logging_f_path ,'w') as f_out:
	f_out.write(stats_buffer)

# # audibly celebrate finished processing of all files
# import time; time.sleep(1); subprocess.call("afplay segmenter/yaas3.mp3", shell='True')
