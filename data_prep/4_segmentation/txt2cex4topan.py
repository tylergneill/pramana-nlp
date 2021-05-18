"""
	Input: Multiple .txt files with:
		[...]/{...} document candidate and candidate grouping markers,
		<...>/(...) structural notes (no distinction), and
		(...)/〈...〉 editorial notes (subtract and add, respectively).
	Output: Single .cex file with two-column #!ctsdata block, with rows:
		identifier	#	modified document contents (resized, split)

	Algorithm (logging and some other small details omitted):

		Read in .txt files from data/input

		For each file:

			1) doc_prep

			Flatten editorial changes to post-correction (remove (...), keep 〈...〉)
			Remove <...>/(...) structural notes
			Remove [...] and {...} markers not followed by content
			Split into {...} sections
			For each {...} section:
				Split into [...] document candidates
				Resize [...] document candidates and modify identifiers accordingly

			2) word_split

			Create global newline-separated buffer with all document contents
			Use single SplitterWrapper call to word-split file contents
				Wrapper first splits string on all punctuation
				Wrapper then splits string again wherever len > 128
				Splitter then splits Sanskrit words
				Wrapper returns reassembled string
					(now sans punctuation and Splitter symbols -, =)

			3) finalize_cex

			Extend identifiers according to lookup table
				(with either common abbreviation or CTS protocol)
			Append results to buffer for .cex #!ctsdata block

		Save buffer to data/output/pramana-nlp_TIMESTAMP.cex

"""

import sys
import os.path
import re
import subprocess
import json
import time
from datetime import datetime, date

from skrutable.splitter.wrapper import Splitter

import resize
from validate import validate_structure, validate_content

force_validate = False
if ("--force_validate" in sys.argv or "-fv" in sys.argv): force_validate = True

validate_only = False
if ("--validate_only" in sys.argv or "-vo" in sys.argv): validate_only = True

resize_only = False
if ("--resize_only" in sys.argv or "-vo" in sys.argv): resize_only = True

input_path = 'data/input/'
output_path = 'data/output/'

text_abbreviations_config_path = 'data/text_abbreviations.json'

with open(text_abbreviations_config_path,'r') as config_file:
	text_abbreviations = json.loads( config_file.read() )
abbrv_type_pref = "common"

logging_path_prefix = 'data/output/logging/'

def log_2col_data(logging_path_suffix, all_doc_identifiers, all_doc_contents):
	full_logging_f_path = os.path.join(logging_path_prefix, logging_path_suffix, fn)
	with open(full_logging_f_path ,'w') as f_out:
		f_out.write('\n'.join(
			[ id + '\t' + c for id, c in zip(all_doc_identifiers, all_doc_contents) ]
			)
		)

stats_buffer = '\t'.join([
	"filename", "docs_orig", "docs_resized", "seg_lines", "tokens"
	]) + '\n' # stats.tsv spreadsheeet header
cex_buffer = '#!ctsdata\n' # .cex file block header

class Section(object):

	def __init__(self):
		self.section_label = ''				# currently stored but not used
		self.doc_identifiers = []
		self.doc_contents = []
		self.doc_count_before_resize = 0	# for logging
		self.doc_count_after_resize = 0		# for logging

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
		['〈([^〉]*?)〉', '\\1'], # accept midline 〈...〉 editorial additions
		['\([^\)]*?\)', ''], # discard (...) philological notes and editorial deletions
		['<[^>]*?>', ''], # discard <...> structural notes
		['\n', ' '], # discard all newlines
		['\[[^\]]*?\]([\[{])', '\\1'], # discard [...] identifiers with no following content (repeat!)
		['{[^}]*?}{', '{'], # discard {...} labels with no following [...] identifiers (or content) (repeat!)
		['(.){', '\\1\n{'], # create newline for each (non-file-initial) {...} label
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


# record starting time
processing_starting_time = datetime.now().time()

# initialize dictionary of section labels by text abbreviation and doc id
section_labels = {}
section_labels_json_fn = 'section_labels.json'

fns = os.listdir(input_path)
fns.sort()
for fn in fns:

	if fn in ['.DS_Store', '.gitkeep']: continue # skip hidden rascals

	"""
	1) doc_prep
	"""

	Spl = Splitter()

	full_input_path = os.path.join(input_path, fn)
	with open(full_input_path, 'r') as f_in:
		raw_text = f_in.read()

	# load appropriate text name abbreviation
	text_name = fn[:fn.rfind('.txt')]
	while text_name not in text_abbreviations[abbrv_type_pref].keys():
		choice = input("Abbreviation not found for '%s'.\nEnter new text_name or 'quit': " % text_name)
		if choice == "quit": exit()
		else: text_name = choice
	text_abbrv = text_abbreviations[abbrv_type_pref][text_name]

	print("validating, precleaning, and parsing %s..." % fn)

	success = validate_structure(raw_text)
	if not(success):
		if force_validate:
			print("%s did not validate (structure) but proceeding anyway..." % fn)
		else:
			choice = input("%s did not validate (structure). continue? (Y\\n) " % fn)
			if choice.lower() in ["n", "no"]: exit()

	success = validate_content(raw_text)
	if not(success):
		if force_validate:
			print("%s did not validate (content) but proceeding anyway..." % fn)
		else:
			choice = input("%s did not validate (content). continue? (Y\\n) " % fn)
			if choice.lower() in ["n", "no"]: exit()

	if validate_only: continue

	text = preclean_1(raw_text)

	raw_section_data = text.split('\n') # divide into {...} sections

	all_Sections = [] # list of Section objects
	all_doc_identifiers = [] # list of strings
	all_doc_contents = [] # list of strings
	section_labels[text_abbrv] = {} # dict of dicts

	for raw_section in raw_section_data:

		ids_and_contents = re.split('(\[[^\]]*?\])', raw_section) # split on [...]

		S = Section()
		S.section_label = ids_and_contents[0].strip()	# store {...} section label
		S.doc_identifiers = ids_and_contents[1::2]		# store [...] document identifiers
		S.doc_contents = ids_and_contents[2::2]			# store document contents

		all_Sections.append(S)

		# save for logging pre-resize documents
		for doc_id, doc_c in zip(S.doc_identifiers, S.doc_contents):
			all_doc_identifiers.append(doc_id)
			all_doc_contents.append(doc_c)

	log_2col_data('1_original_doc_candidates/', all_doc_identifiers, all_doc_contents)

	print("resizing %s..." % fn)

	doc_count_before_resize = len(all_doc_contents)

	# clear and build again from resizing results
	all_doc_contents = []
	all_doc_identifiers = []

	for S in all_Sections:

		S.resize_docs()

		for doc_id, doc_c in zip(S.doc_identifiers, S.doc_contents):
			all_doc_identifiers.append(doc_id)
			all_doc_contents.append(doc_c)

			# save section label for lookup later
			section_labels[text_abbrv][doc_id] = S.section_label


	doc_count_after_resize = len(all_doc_contents)

	log_2col_data('2_resized_docs/', all_doc_identifiers, all_doc_contents)

	# also log section_labels dict as json
	full_f_path = os.path.join(output_path, section_labels_json_fn)
	with open(full_f_path,'w') as f_out:
		json_object = {}
		json_object["section_labels"] = section_labels
		json.dump(json_object, f_out, indent=4, ensure_ascii=False)

	if resize_only: continue

	"""
	2) word_split
	"""

	print("word-splitting %s..." % fn)

	# join and preclean for word-splitting
	presegmentation_content = '\n'.join(all_doc_contents)
	presegmentation_content = preclean_2(presegmentation_content)

	log_2col_data('3_pre-word-split/', all_doc_identifiers, all_doc_contents)

	# first do manual segmentation
	presegmentation_content = presegmentation_content.replace('-', ' ')

	# use Splitter
	postsegmentation_content = Spl.split(presegmentation_content, prsrv_punc=False)

	# can use some final cleaning...
	postsegmentation_content = re.sub(' +', ' ', postsegmentation_content)
	# ...

	# restore back to being list
	all_doc_contents = postsegmentation_content.split('\n')

	log_2col_data('4_post-word-split/', all_doc_identifiers, all_doc_contents)

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

	modified_ids = [text_abbrv + '_' + id for id in all_doc_identifiers]

	for id, content in zip(modified_ids, all_doc_contents):
		id = re.sub('[\[\]]','', id) # finally remove square brackets
		cex_buffer += id + '#' + content + '\n'

if validate_only:
	print("validate_only == True, exiting.")
	exit()

# output stats for all files
full_logging_f_path = os.path.join(logging_path_prefix, 'stats.tsv')
with open(full_logging_f_path ,'w') as f_out:
	f_out.write(stats_buffer)



# record ending time
processing_ending_time = datetime.now().time()

# report total processing time on command line
delta = datetime.combine(
	date.today(),
	processing_ending_time) - datetime.combine(date.today(),
	processing_starting_time
	)
print("%s finished in %d:%d" % (
	os.path.basename(__file__),
	delta.seconds//60, delta.seconds%60)
	)

# prepare output file timestamp
finish_time_obj = datetime.now()
timestamp = finish_time_obj.strftime("%Y-%m-%d-%H-%M")

# save results
cex_output_f_path = os.path.join(output_path, 'pramana-nlp_%s.cex' % timestamp)
with open(cex_output_f_path, 'w') as f_out:
	f_out.write(cex_buffer)

# celebrate
time.sleep(1)
subprocess.call("afplay yaas3.mp3", shell='True')
