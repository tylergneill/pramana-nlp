import sys
import re
import json

mode = None # whether structure or content validation
pause_between_problems = False # extra option for verbose structure validation
output_bracketless = False # optional output to accompany verbose content validation
prompt_update_ngrams = False # option to accept all remaining "problem" ngrams and add to json

max_ngram_len = 2 # anything above 3 seems like overkill, but starting with 2 for now
flagged_ngrams_txt_fn = 'validation_files/flagged_ngrams.txt'
accepted_ngrams_json_fn = 'validation_files/accepted_ngrams.json'
bracketless_content_txt_fn = 'validation_files/bracketless_content.txt'

"""
structure validation functions

together ensure proper bracket pairing
"""
abs = '\[\]{}<>\(\)〈〉' # all_brackets_string
empty_bracket_pair_regex = '(\[\])|({})|(<>)|(\(\))|(〈〉)'
full_deletable_bracket_pair_regex = '(\[[^%s]*?\])|({[^%s]*?})|(<[^%s]*?>)|(\([^%s]*?\))' % tuple([abs]*4)
full_keepable_bracket_pair_regex = '〈([^%s]*?)〉' % abs

def view_problem_brackets(problem_brackets, raw_input_text):

	lefts = ['[', '{', '<', '(', '〈']
	rights = [']', '}', '>', ')', '〉']
	l_rs = zip(lefts,rights)
	corr_memb = {}
	for l, r in l_rs: corr_memb[l] = r; corr_memb[r] = l

	for bracket in problem_brackets:

		if bracket in ['[','(',']',')']: # chars need to be escaped
			regex = '\%s[^\%s]*?\%s' % (bracket, corr_memb[bracket], bracket)
		else: # chars don't need to be escaped
			regex = '%s[^%s]*?%s' % (bracket, corr_memb[bracket], bracket)

		print("problem bracket: ", bracket)
		print("find with this regex: ", regex)
		result = re.search(regex, raw_input_text) # find first instance
		try:
			print("context hint:\n", result.group())
		except: print('not a faulty bracket pair, look for bracket nesting...')
		print("\n****\n")
		if pause_between_problems: input()

# def check_clean_surroundings(content):
# 	print("# of non-line-initial [{< : ", len(re.findall('[^\n][\[{<]',content)))
# 	print("# of non-line-final ]}> : ", len(re.findall('[\]}>][^\n]',content)))
# 	print()

def validate_structure(raw_input_text, verbose=False):

	# if verbose: check_clean_surroundings(raw_input_text)

	brackets_only = re.sub('[^\[\]{}<>\(\)〈〉]', '', raw_input_text) # remove all chars besides brackets

	# remove valid empty bracket pairs, iteratively in case nested
	# leave behind only unsearched bracket chars
	while bool( re.search(empty_bracket_pair_regex, brackets_only) ) == True:
		brackets_only = re.sub(empty_bracket_pair_regex, '', brackets_only)

	if brackets_only == '':
		if verbose: print("no problem brackets, structure validated successfully\n")
		return 1
	else:
		if verbose:
			print("problematic remaining brackets:", brackets_only, '\n')
			view_problem_brackets(brackets_only, raw_input_text)
		return 0


"""
content validation function (only the one, not yet modularized)
"""

def get_ngrams_with_freqs(text, n):

	ngram_freqs = {} # dict contains multiple lists of ngrams (of lens 1...n)

	for n in range(1,n+1):

		# get list of ngrams for a given n
		ngram_list = [ text[i:i+n] for i in range(len(text)-n+1) ]

		# dedupe and sort
		unique_ngram_list = list(set(ngram_list))
		unique_ngram_list.sort()

		# count frequencies too
		ngram_freqs[n] = {}
		for u_ng in unique_ngram_list:
			ngram_freqs[n][u_ng] = text.count(u_ng)

	return ngram_freqs

def validate_content(raw_input_text, verbose=False):

	if verbose:
		print('comparing content of input text against known ngrams ...')

	content = raw_input_text

	# remove deletable brackets and their contents, iteratively in case nested
	# leave behind only text content
	# and check twice in case of lots of nesting

	for i in range(2):

		while bool( re.search(full_deletable_bracket_pair_regex, content) ) == True:
			content = re.sub(full_deletable_bracket_pair_regex, '', content)

		# keep content of keepable brackets
		while bool( re.search(full_keepable_bracket_pair_regex, content) ) == True:
			content = re.sub(full_keepable_bracket_pair_regex, '\\1', content)

	# clean up extra whitespace
	regex_replacements = [
		[' *(\n+) *', '\\1'], # extraneous space adjacent to newline
		['\n{2,}', '\n\n'], # extraneous newline (x2 max)
		[' {2,}', ' '], # duplicate space
		('\A\s*', ''),	# file-initial whitespace
		('\s*\Z', ''),	# file-final whitespace
	]
	for r_r in regex_replacements:
		content = re.sub(r_r[0], r_r[1], content)

	# useful for inspecting what actual content is being measured
	if output_bracketless == True:
		with open(bracketless_content_txt_fn, 'w') as f_out:
			f_out.write(content)

	# initialize dict for flagging unrecognized ngrams
	curr_flagged_ngrams_with_freqs = {}
	for i in range(1,max_ngram_len+1):
		curr_flagged_ngrams_with_freqs[i] = {}

	try:
		# load
		with open(accepted_ngrams_json_fn,'r') as f_in:
			accepted_ngrams = json.load(f_in)["accepted_ngrams"]
	except FileNotFoundError:
		# initialize
		accepted_ngrams = {}
		for i in range(1,max_ngram_len+1):
			accepted_ngrams[str(i)] = [] # strings for keys for sake of json dict

	# get all unique ngrams of lens 1...max_ngram_len
	text_ngram_freqs = get_ngrams_with_freqs(content, max_ngram_len) # dict with sorted 1-grams and 2-grams and freqs

	# compare against accepted_ngrams and flag unrecognized ones
	for i in range(1,max_ngram_len+1):
		for ng in text_ngram_freqs[i].keys():
			if ng not in accepted_ngrams[str(i)]: # dict from json files has strings for keys
				curr_flagged_ngrams_with_freqs[i][ng] = text_ngram_freqs[i][ng]

			# used to also treat certain chars differently and look for > 128-char sequences

			# tricky_chars = ['_', '-', '\t']
			# # also add: more as found
			# for c in tricky_chars:
			# 	if c in content:
			# 		if verbose: print("watch out for %s '%s': %d" % (repr(c), c, content.count(c)))

			# chunks = ( ( content.replace('\n',' ') ).replace('_',' ') ).split(' ')
			# chunks_gt_128 = []
			# for chunk in chunks:
			# 	if len(chunk) > 128: chunks_gt_128.append(chunk)
			# if verbose:
			# 	if chunks_gt_128 != []: print("# chunks > 128:", len(chunks_gt_128))
			# 	for chunk in chunks_gt_128: print(chunk)

	# create parallel dict with each sub-dict sorted for inspection in txt output
	curr_flagged_ngrams_sorted_by_freqs = {}
	for i in range(1,max_ngram_len+1):
		curr_flagged_ngrams_sorted_by_freqs[i] = dict(sorted(curr_flagged_ngrams_with_freqs[i].items(), key=lambda item: item[1], reverse=True))

	# create parallel dict without freqs for appending to json
	curr_flagged_ngrams = {}
	for i in range(1,max_ngram_len+1):
		curr_flagged_ngrams[i] = list(curr_flagged_ngrams_with_freqs[i].keys())

	# later can also aggregate collected freq info corpus-wide for more sensitive flagging

	# count flagged ngrams
	num_flagged_ngrams = 0
	for k in curr_flagged_ngrams.keys():
		num_flagged_ngrams += len(curr_flagged_ngrams[k])

	if num_flagged_ngrams != 0:

		if verbose: print('content did not validate, new ngrams flagged (see file \"%s\")' % flagged_ngrams_txt_fn)
		with open(flagged_ngrams_txt_fn,'w') as f_out:
			for i in range(1,max_ngram_len+1):
				if i not in curr_flagged_ngrams_sorted_by_freqs.keys(): continue
				f_out.write( '\n'.join(
					[ str(curr_flagged_ngrams_sorted_by_freqs[i][k]) + '\t' + repr(k) for k in curr_flagged_ngrams_sorted_by_freqs[i].keys()]
				) )
				f_out.write('\n')

		if prompt_update_ngrams:
			choice = input('remember all new ngrams (add to file \"%s\")? (Y/[n]) ' % accepted_ngrams_json_fn)
			if choice == 'Y':

				# add new ngrams to dict
				for i in range(1,max_ngram_len+1):
					if i not in curr_flagged_ngrams.keys(): continue
					for ngram in curr_flagged_ngrams[i]:
						if str(i) not in accepted_ngrams.keys(): continue
						if ngram not in accepted_ngrams[str(i)]:
							accepted_ngrams[str(i)].append(ngram)
						accepted_ngrams[str(i)].sort()

				# overwrite json
				with open(accepted_ngrams_json_fn,'w') as f_out:
					json_object = {}
					json_object["accepted_ngrams"] = accepted_ngrams # updated
					json.dump(json_object, f_out, indent=4, ensure_ascii=False)

				# clean up appearance a little more: keep ngram lists on one line each
				with open(accepted_ngrams_json_fn,'r') as f_in:
					json_string = f_in.read()
					json_string = json_string.replace(",\n            ", ", ")
				with open(accepted_ngrams_json_fn,'w') as f_out:
					f_out.write(json_string)

		return 0

	elif num_flagged_ngrams == 0:
		if verbose: print("content validated successfully")
		return 1


if __name__ == '__main__':

	if len(sys.argv) == 1:
		print("argument needed")
		exit()

	fn = sys.argv[1]
	if fn[-4:] != ".txt":
		print(".txt needed as first argument")
		exit()

	if not ("-s" in sys.argv or "-c" in sys.argv):
		print("which mode? ( -s / -c )")
		exit()
	elif "-s" in sys.argv:
		mode = 'structure'
	elif "-c" in sys.argv:
		mode = 'content'

	if "--pause" in sys.argv:
		pause_between_problems = True

	if "--output_bracketless" in sys.argv:
		output_bracketless = True

	if ("--prompt_update_ngrams" in sys.argv
		or "-u" in sys.argv
		):
		prompt_update_ngrams = True

	with open(fn,'r') as f_in:
		raw_input_text = f_in.read()

	if mode == 'structure':
		validate_structure(raw_input_text, verbose=True)
	elif mode == 'content':
		validate_content(raw_input_text, verbose=True)
