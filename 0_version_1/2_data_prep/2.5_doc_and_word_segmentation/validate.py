#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

mode = None # whether structure or content validation
pause_between_problems = False # extra option for verbose structure validation
output_bracketless = False # optional output to accompany verbose content validation

"""
structure validation functions
"""

def find_problem_brackets(content, verbose):
	just_brackets = re.sub('[^\[\]{}<>\(\)]','',content)
	minus_parentheses_pairs = re.sub('\(\)','',just_brackets)
	remaining_problem_brackets = re.sub('\[\]|{}|<>','',minus_parentheses_pairs)
	if verbose:
		if remaining_problem_brackets == '': print "no problem brackets"
		else: print "set of problem brackets:", remaining_problem_brackets
		print 
	return remaining_problem_brackets

def view_problems(problem_brackets, content):

	lefts = ['[', '{', '<', '(']
	rights = [']', '}', '>', ')']
	l_rs = zip(lefts,rights)
	corr_memb = {}
	for l, r in l_rs: corr_memb[l] = r; corr_memb[r] = l

	print "problems to fix:"; print
	for bracket in problem_brackets:
		if bracket in ['[','(',']',')']:
			regex = '\%s[^\%s]*?\%s' % (bracket, corr_memb[bracket], bracket)
		else: regex = '%s[^%s]*?%s' % (bracket, corr_memb[bracket], bracket)
		print "bracket = ", bracket; print "regex = ", regex
		result = re.search(regex, content)
		try: print result.group()
		except: print 'not a faulty pair, look for nesting...'
		print
		if pause_between_problems: raw_input()

def check_clean_surroundings(content):
	print "# of non-line-initial [{< : ", len(re.findall('[^\n][\[{<]',content))
	print "# of non-line-final ]}> : ", len(re.findall('[\]}>][^\n]',content))
	print

def validate_structure(fn, verbose=False):
	f = open(fn,'r'); content = f.read(); f.close()

	if verbose: check_clean_surroundings(content)

	problem_brackets = find_problem_brackets(content, verbose)

	if problem_brackets != '':
		if verbose: view_problems(problem_brackets, content)
		return 0
	
	if verbose: print "structure validated, all good"
	return 1


"""
content validation function (only the one, not yet modularized)
"""

def validate_content(fn, verbose=False):
	f = open(fn,'r'); content = f.read(); f.close()
	content = content.decode('utf-8')
	
	if verbose: print "looking for illegal characters and sequences..."

	# remove non-text
	regex_replace = [
	['\[[^\]]*?\]', ''], 
	['{[^}]*?}', ''], 
	['<[^>]*?>', ''], 
	['\n\([^\)]*?\) *', '\n'], 
	[' *\([^\)]*?\)\n', '\n'], 
	['\([^\)]*?\)', ''], 
	]
	for r_r in regex_replace: content = re.sub(r_r[0], r_r[1], content)

	if output_bracketless == True:
		f2 = open(fn[:-4] + '_bracketless.txt', 'w')
		f2.write(content.encode('utf-8'))
		f2.close()
  
	total_instances = 0

	normal_chars = ['a', 'b', 'c', 'd', 'e', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', u'ā', u'ī', u'ū', u'ṛ', 'ṝ'.decode('utf-8'), u'ḷ', 'ḹ'.decode('utf-8'), u'ṅ', u'ñ', u'ṭ', u'ḍ', u'ṇ', u'ś', u'ṣ', u'ḥ', u'ṃ', ' ', '"', "'", '!', '_', '-', '\t', '|', '/', '.', ',', ';', ':', '?', '—'.decode('utf-8'), '\n', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

	illegal_chars = ['`', '~', '@', '#', '$', '%', '^', '&', '*', '+', '\\', '=', '‘'.decode('utf-8'), '’'.decode('utf-8'), '“'.decode('utf-8'), '”'.decode('utf-8'), '\r', '–'.decode('utf-8'), 'ǀ'.decode('utf-8'), '…'.decode('utf-8')] # en-dash
	# also add: more as found
	illegal_chars_found = []
	for c in illegal_chars:
		if c in content:
			if verbose: print "found illegal character: %s '%s' (%d)" % (repr(c), c, content.count(c))
			total_instances += content.count(c)
			illegal_chars_found.append(c)

	# also add: more as found
	other_chars_found = []
	for c in content:
		if c not in normal_chars + illegal_chars + other_chars_found:
			if verbose: print "found other character: %s '%s' (%d)" % (repr(c), c, content.count(c))
			total_instances += content.count(c)
			other_chars_found.append(c)

	illegal_sequences = [" \n", "\n "]
	# also add: all decomposed diacritic combinations
	# also add: more as found
	illegal_sequences_found = []
	for s in illegal_sequences:
		if s in content:
			if verbose: print "found illegal sequence: %s '%s' (%d)" % (repr(s), s, content.count(s))
			total_instances += content.count(s)
			illegal_sequences_found.append(s)

	if verbose: print; print "warnings: ..."; print

	tricky_chars = ['_', '-', '\t']
	# also add: more as found
	for c in tricky_chars:
		if c in content:
			if verbose: print "watch out for %s '%s': %d" % (repr(c), c, content.count(c))

	chunks = ( ( content.replace('\n',' ') ).replace('_',' ') ).split(' ')
	chunks_gt_128 = []
	for chunk in chunks:
		if len(chunk) > 128: chunks_gt_128.append(chunk)	
	if verbose:
		if chunks_gt_128 != []: print "# chunks > 128:", len(chunks_gt_128)
		for chunk in chunks_gt_128: print chunk

	if illegal_chars_found + other_chars_found + illegal_sequences_found != []:
		if verbose: print "total things to deal with:", total_instances
		return 0

	if verbose: print; print "warnings complete."; print
		
	if verbose: print "content validated, all good"
	return 1

	
if __name__ == '__main__':

	if len(sys.argv) == 1: print "argument, please"; exit()

	fn = sys.argv[1]
	if fn[-4:] != ".txt": print ".txt as first argument, please"; exit()

	if not ("--s" in sys.argv or "--c" in sys.argv): print "which mode?"; exit()
	elif "--s" in sys.argv: mode = 'structure'
	elif "--c" in sys.argv: mode = 'content'

	if "--pause" in sys.argv: pause_between_problems = True

	if "--output_bracketless" in sys.argv: output_bracketless = True

	if mode == 'structure': validate_structure(fn, verbose=True)
	elif mode == 'content': validate_content(fn, verbose=True)
