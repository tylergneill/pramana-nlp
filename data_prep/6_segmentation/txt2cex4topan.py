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
from skrutable.splitter.wrapper import Splitter

import resize
# import validate

input_path = 'data/input/'
output_path = 'data/output/'

logging_path_prefix = 'data/output/logging/'
stats_buffer = '\t'.join([
	"filename", "docs_orig", "docs_resized", "seg_lines", "tokens"
	]) + '\n' # header row

# initialize CTS file buffer here...


class Section(object):

	def __init__(self):
		self.section_label = ''
		self.doc_identifers = []
		self.doc_contents = []
		self.doc_count_before_resize = 0
		self.doc_count_after_resize = 0
		self.word_split_line_count = 0
		self.token_count = 0

	def preclean(self):
		for i in range(len(self.doc_contents)):
			regex_replace = [
			# delete (...), punctuation adjacent to numbers, numbers, quotation marks, extra spacing
			['\([^\)]*?\)', ''],
			['([\|/])+([\d\.,– ]+)(\\1)+', '\\1'],
			['[\d"“”\t]', ''],
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

	Spl = Splitter()

	full_input_path = os.path.join(input_path, fn)
	with open(full_input_path, 'r') as f_in:
		f_data = f_in.read()

	print("validating and parsing %s..." % fn)

	# do structural validation here...

	# could also do content validation here...

	# do some structural cleaning
	regex_replacement = [
		['<[^>]*?>', ''], # discard <...>
		['\([^\)]*?\)', ''], # discard (...)
		# ['\(([^\)]*?)\)', '\\1'], # keep (...)
		['\n', ''], # discard all newlines
		['\[[^\]]*?\]([\[{])', '\\1'], # discard [...] identifiers with no content (repeat!)
		['{[^}]*?}{', '{'], # discard {...} labels with no content (repeat!)
		['(.){','\\1\n{'], # create newline for each (non-file-initial) {...}
	]
	to_repeat = ['\[[^\]]*?\]\[', '\{[^\}]*?\}\{']
	for r_r in regex_replacement:
		f_data = re.sub(r_r[0], r_r[1], f_data)
		if r_r[0] in to_repeat: # repeat as necessary
			while bool( re.search(r_r[0], f_data) ) == True:
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

		all_Sections.append(S)

		for doc_identifier in S.doc_identifers:
			all_doc_identifiers.append(doc_identifier)
		for doc_content in S.doc_contents:
			all_doc_contents.append(doc_content)

	# log
	logging_path_suffix = '1_original_doc_candidates/'
	full_logging_f_path = os.path.join(logging_path_prefix, logging_path_suffix, fn)
	with open(full_logging_f_path ,'w') as f_out:
		f_out.write('\n'.join(
			[ id + '\t' + c for id, c in zip(all_doc_identifiers, all_doc_contents) ]
			)
		)

	print("precleaning and resizing %s..." % fn)

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
	logging_path_suffix = '2_resized_docs/'
	full_logging_f_path = os.path.join(logging_path_prefix, logging_path_suffix, fn)
	with open(full_logging_f_path ,'w') as f_out:
		f_out.write('\n'.join(
			[ id + '\t' + c for id, c in zip(megaS.doc_identifers, megaS.doc_contents) ]
			)
		)

	print("word-splitting %s..." % fn)

	# presegmentation_content = '\n#\n'.join(megaS.doc_contents)
	presegmentation_content = '\n'.join(megaS.doc_contents)

	# any remaining '-' must have been intentionally placed by me for segmentation
	presegmentation_content = presegmentation_content.replace('-', ' ')

	postsegmentation_content = Spl.split(presegmentation_content, prsrv_punc=True)

	# count lines and tokens
	megaS.word_split_line_count = Spl.line_count_during_split
	megaS.token_count = Spl.token_count

	# reincorporate treated content back into master Section object
	megaS.doc_contents = postsegmentation_content.split('\n')

	# log
	logging_path_suffix = '3_word-split_docs/'
	full_logging_f_path = os.path.join(logging_path_prefix, logging_path_suffix, fn)
	with open(full_logging_f_path ,'w') as f_out:
		f_out.write('\n'.join(
			[ id + '\t' + c for id, c in zip(megaS.doc_identifers, megaS.doc_contents) ]
			)
		)

 	# convert doc_identifers to CTS URNS here...
	# use tsv lookup table ...

	# add all results to CTS file buffer ...
	# simple join...

	# record individual file stats

	stats_buffer += '\t'.join([
		fn,
		str(megaS.doc_count_before_resize),
		str(megaS.doc_count_after_resize),
		str(megaS.word_split_line_count),
		str(megaS.token_count)
		]) + '\n'

# output stats for all files
full_logging_f_path = os.path.join(logging_path_prefix, 'stats.tsv')
with open(full_logging_f_path ,'w') as f_out:
	f_out.write(stats_buffer)

# # audibly celebrate finished processing of all files
# import time; time.sleep(1); subprocess.call("afplay segmenter/yaas3.mp3", shell='True')
