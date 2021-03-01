"""
	Input: Multiple .txt with [...]/{...} document candidates and <...>/(...) notes
	Output: Single .cex with identifiers and modified document contents.

	Algorithm (logging and some other small details omitted):

		Read in .txt files from data/input

		For each file:

			1) doc_prep

			Remove <...>/(...) notes
			Remove [...] identifiers and {...} labels not followed by content
			Split into {...} sections
			For each {...} section:
				Split into [...] document candidates
				Resize [...] document candidates and modify identifiers accordingly

			2) word_split

			Create global newline-separated buffer with all document contents
			Use single SplitterWrapper call to word-split file contents (can also maintain most punctuation)
				Wrapper first splits on all punctuation
				Wrapper also splits again wherever len > 128
				Splits words
				Reassembles saved line-breaks (& punctuation) and returns result

			3) finalize_cex

			Remove punctuation and Splitter symbols (-, =)
			Extend identifiers according to CTS
			Append results to buffer for .cex #!ctsdata block

		Combine and save results to .cex file in data/output/pramana-nlp_TIMESTAMP.cex

"""

import sys
import os.path
import re
import subprocess

from skrutable.splitter.wrapper import Splitter

import resize
from validate import validate_structure, validate_content

input_path = 'data/input/'
output_path = 'data/output/'

logging_path_prefix = 'data/output/logging/'

def log(logging_path_suffix, all_doc_identifiers, all_doc_contents):
	full_logging_f_path = os.path.join(logging_path_prefix, logging_path_suffix, fn)
	with open(full_logging_f_path ,'w') as f_out:
		f_out.write('\n'.join(
			[ id + '\t' + c for id, c in zip(all_doc_identifiers, all_doc_contents) ]
			)
		)

stats_buffer = '\t'.join([
	"filename", "docs_orig", "docs_resized", "seg_lines", "tokens"
	]) + '\n' # stats.tsv spreadsheeet header
# cex_buffer = '#!ctsdata\n' # .cex file header

class Section(object):

	def __init__(self):
		self.section_label = ''
		self.doc_identifiers = []
		self.doc_contents = []
		self.doc_count_before_resize = 0
		self.doc_count_after_resize = 0
		self.word_split_line_count = 0
		self.token_count = 0

	def resize_docs(self):
		"""
			Resizes self.doc_contents (and updates self.doc_identifiers) based on
				lower bound = resize.min_doc_size
				upper bound = resize.max_doc_size
					(generally, but also a few cases of min_doc_size + max_doc_size...)
		"""
		temp_content_L, temp_identifier_L = resize.split_big_docs(self.doc_contents, self.doc_identifiers)
		self.doc_contents, self.doc_identifiers = resize.combine_small_docs(temp_content_L, temp_identifier_L)

def preclean_1(text):
	"""
		Cleans up structure in anticipation of doc-resizing and word-splitting.
	"""
	regex_replacement = [
		['([^\n])(\[[^\]]*?\])([^\n])', '\\1\\2'], # accept midline [...] editorial additions
		['(\[[^\]]*?\])([^\n])', '\\1\\2'], # accept midline [...] editorial additions
		['<[^>]*?>', ''], # discard <...> structural notes
		['\([^\)]*?\)', ''], # discard (...) philological notes and editorial deletions
		# ['\(([^\)]*?)\)', '\\1'], # keep (...)
		['\n', ' '], # discard all newlines
		['\[[^\]]*?\]([\[{])', '\\1'], # discard [...] identifiers with no content (repeat!)
		['{[^}]*?}{', '{'], # discard {...} labels with no content (repeat!)
		['(.){', '\\1\n{'], # create newline for each (non-file-initial) {...}
	]
	to_repeat = [
		'\[[^\]]*?\]([\[{])',
		'{[^}]*?}{',
	]
	for r_r in regex_replacement:

		text = re.sub(r_r[0], r_r[1], text)

		# repeat as necessary
		if r_r[0] in to_repeat:
			while bool( re.search(r_r[0], text) ) == True:
				text = re.sub(r_r[0], r_r[1], text)

	return text

def preclean_2(text):
	"""
		Cleans up punctuation in anticipation of word-splitting.
	"""
	regex_replace = [
		['([\|/])+([\d\.,– ]+)(\\1)+', '\\1'], # discard punctuation adjacent to numbers
		['[\d"“”\t]', ''], # discard numbers, quotation marks
		[' {2,}', ' '], # discard extra spacing
		['([\|/\.] ?)+', '\\1'], # simplify duplicate punctuation (also with intervening spaces)
		[u'([^ ])([\|/\.,;:—\?])', '\\1 \\2'], # space out punctuation as necessary
		[u'([\|/\.,;:—\?])([^ ])', '\\1 \\2'], # space out punctuation as necessary
	]
	for r_r in regex_replace: text = re.sub(r_r[0], r_r[1], text)
	return text


fns = os.listdir(input_path)
fns.sort()
for fn in fns:

	if fn in ['.DS_Store']: continue # skip those macOS rascals

	"""
	1) doc_prep
	"""

	Spl = Splitter()

	full_input_path = os.path.join(input_path, fn)
	with open(full_input_path, 'r') as f_in:
		text = f_in.read()

	print("validating, precleaning, and parsing %s..." % fn)

	success = validate_structure(text)
	if not(success):
		import pdb; pdb.set_trace()
		# maybe create setting for default action here

	success = validate_content(text)
	if not(success):
		import pdb; pdb.set_trace()
		# maybe create setting for default action here

	text = preclean_1(text)

	raw_section_data = text.split('\n') # divide into {...} sections

	all_Sections = [] # list of Section objects
	all_doc_identifiers = [] # list of strings
	all_doc_contents = [] # list of strings

	for raw_section in raw_section_data:

		ids_and_contents = re.split('(\[[^\]]*?\])', raw_section) # split on [...]

		S = Section()
		S.section_label = ids_and_contents[0]		# store {...} section label
		S.doc_identifiers = ids_and_contents[1::2]	# store [...] document identifiers
		S.doc_contents = ids_and_contents[2::2]		# store document contents

		all_Sections.append(S)

		for s_m, s_c in zip(S.doc_identifiers, S.doc_contents):
			all_doc_identifiers.append(s_m)
			all_doc_contents.append(s_c)

	log('1_original_doc_candidates/', all_doc_identifiers, all_doc_contents)

	print("resizing %s..." % fn)

	doc_count_before_resize = len(all_doc_contents)

	# clear and build again from resizing results
	all_doc_contents = []
	all_doc_identifiers = []

	for S in all_Sections:

		S.resize_docs()

		for s_m, s_c in zip(S.doc_identifiers, S.doc_contents):
			all_doc_identifiers.append(s_m)
			all_doc_contents.append(s_c)

	doc_count_after_resize = len(all_doc_contents)

	log('2_resized_docs/', all_doc_identifiers, all_doc_contents)

	"""
	2) word_split
	"""

	print("word-splitting %s..." % fn)

	# join and preclean for word-splitting
	presegmentation_content = '\n'.join(all_doc_contents)
	presegmentation_content = preclean_2(presegmentation_content)

	log('3_pre-word-split/', all_doc_identifiers, all_doc_contents)

	# first do manual segmentation
	presegmentation_content = presegmentation_content.replace('-', ' ')

	# use Splitter
	postsegmentation_content = Spl.split(presegmentation_content, prsrv_punc=True)

	# can use some final cleaning...
	postsegmentation_content = re.sub(' +', ' ', postsegmentation_content)
	# ...

	# restore back to being list
	all_doc_contents = postsegmentation_content.split('\n')

	log('4_post-word-split/', all_doc_identifiers, all_doc_contents)

	# record individual file stats

	stats_buffer += '\t'.join([
		fn,
		str(doc_count_before_resize),
		str(doc_count_after_resize),
		str(Spl.line_count_during_split),
		str(Spl.token_count)
		]) + '\n'

	"""
	3) finalize_cex
	"""

 	# convert doc_identifiers to CTS URNS here...
	# use tsv lookup table ...

	# add all results to CTS file buffer ...
	# simple join...

# output stats for all files
full_logging_f_path = os.path.join(logging_path_prefix, 'stats.tsv')
with open(full_logging_f_path ,'w') as f_out:
	f_out.write(stats_buffer)

# output .cex combining all data

# # audibly celebrate finished processing of all files
# import time; time.sleep(1); subprocess.call("afplay segmenter/yaas3.mp3", shell='True')
