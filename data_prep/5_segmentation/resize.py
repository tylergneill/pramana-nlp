import re

min_doc_size = 300 # char len
max_doc_size = 1000 # char len
crp = 0.8 # center range parameter for split (= possible % range from center)

doc_splitpoint_regexes = [
	u'[\.\?\|/]',
	u'[\.\?\|/]',
	u'[;—,]',
	u'[;—,]',
	u'[ ]',
]

# NOT USING ANYMORE
# def resize(doc_L, identifer_L):
# 	doc_L, identifer_L = split_big_docs(doc_L, identifer_L)
# 	return combine_small_docs(doc_L, identifer_L)

def no_small_docs(doc_L):
	for l in [len(x) for x in doc_L]:
		if l < min_doc_size:
			return False
	else:
		return True

def no_big_docs(doc_L):
	for l in [len(x) for x in doc_L]:
		if l > max_doc_size:
			return False
	else:
		return True

"""
Splitting functions (4):
	split_big_docs()
	attempt_splits()
	split_unit()
	find_midpoint()
"""

# VERY OLD
# def split_big_docs(doc_L, identifer_L):
# 	"""
# 	Guarantees successful split through cascade algorithm.
# 	Also simultaneously manages identifers during splitting.
# 	Cascade algorithm:
# 	1. Then try splitting at major punctuation [\.\?\|/] with max_length at 100%.
# 	2. Then try splitting at major punctuation [\.\?\|/] with max_length at 110%.
# 	3. Then try splitting at minor punctuation [;—,] with max_length at 100%.
# 	4. Then try splitting at minor punctuation [;—,] with max_length at 120%.
# 	5. Then just split at space [ ] with max_length at 100%.
# 	Returns resulting list of new docs along with respective doc identifers
# 	"""
# 	split_settings = [
# 		(u'[\.\?\|/]', 1.0 * b),
# 		(u'[\.\?\|/]', 1.1 * b),
# 		(u'[;—,]', 1.0 * b),
# 		(u'[;—,]', 1.2 * b),
# 		(u'[ ]', 1.0 * b),
# 	]
# 	for c in split_settings:
# 		doc_L2, identifer_L2 = attempt_splits(doc_L, identifer_L, c[0], c[1])
# 		if no_big_docs(doc_L2): return doc_L2, identifer_L2
#
# 	print "ERROR, ALL SPLIT ATTEMPTS FAILED"; exit()


def split_big_docs(doc_L, identifer_L):
	"""
	max_len will be between 1.0 * max_doc_size and 1.2 * max_doc_size
	# THEN IT'S NOT 'MAX' NOW IS IT?? FIX!
	"""

	if no_big_docs(doc_L): return doc_L, identifer_L

	# import pdb; pdb.set_trace()
	doc_L2 = []
	identifer_L2 = []
	for (doc, identifer) in zip(doc_L, identifer_L):

		if len(doc) <= max_doc_size:
			doc_L2.append(doc) # save appropriately sized doc
			identifer_L2.append(identifer) # also append current identifer_L

		else:

			# search for middle-most puncutation
			results = split_unit(doc)

			for i, r in enumerate(results):

				new_doc = r;
				doc_L2.append(new_doc)

				new_identifer = identifer[:-1].replace('_',u'–') + '^%d]' % (i+1)
				# logging.debug( identifer.ljust(35) + '(split)'.ljust(35) + new_identifer )
				identifer_L2.append(new_identifer)

	return doc_L2, identifer_L2 # if len(doc_L2) == 1, means that split failed

def split_unit(unit, splitpoint_regexes = doc_splitpoint_regexes, max_len = max_doc_size):
	"""
	Recursively split unit into smaller documents according to splitpoint_regex until all resulting docs conform to max_len.
	unit may be a doc (when adjusting docs) or a line (when preparing for segmenter).
	Return list of resulting docs.
	"""
	# remove initial and final spaces
	unit = re.sub(u"(^ *| *$)",'', unit)

	if len(unit) <= max_len:
		return [unit]
	else:
		for splitpoint_regex in splitpoint_regexes:
			midpoint = find_midpoint(unit, splitpoint_regex)
			if midpoint > (1.0 - (1.0 - crp) / 2) * len(unit) or midpoint < ((1.0 - crp) / 2) * len(unit): continue
			else: break

		part_a = split_unit( unit[ : midpoint + 1] , splitpoint_regexes, max_len)
		part_b = split_unit( unit[midpoint + 1 : ] , splitpoint_regexes, max_len)
		return part_a + part_b

def find_midpoint(unit, splitpoint_regex):
	"""
	Determine position of centermost legal split of unit based on splitpoint_regex.
	Return integer index.
	"""

	all_indices = [m.start() for m in re.finditer(splitpoint_regex, unit)]
	distances_from_middle = [abs(i - len(unit)/2) for i in all_indices]
	try:
		most_middle_index = all_indices[distances_from_middle.index(min(distances_from_middle))]
		return most_middle_index
	except ValueError:
		return 0

"""
Combining functions (3):
	combine_small_docs()
	combine_two_docs()
	combine_two_identifers()
"""

def combine_small_docs(doc_L, identifer_L):

	if no_small_docs(doc_L) or len(doc_L) <= 1: return doc_L, identifer_L

	doc_L2 = ['']
	identifer_L2 = ['']

	for i, (doc, identifer) in enumerate(zip(doc_L, identifer_L)):

		if len(doc_L[i]) >= min_doc_size:
			if doc_L2[-1] == '':
				doc_L2[-1] = doc_L[i]
				identifer_L2[-1] = identifer_L[i]
			else:
				doc_L2.append(doc_L[i])
				identifer_L2.append(identifer_L[i])

		else:

			# something already kept as long enough?
			if len(doc_L2[-1]) > 0:

				# if so, want to add to left
				# but only if left is smaller than what's ahead
				# so first, try looking ahead
				try:
					doc_L[i+1] # check whether next exists

					# if here, next exists, so now compare

					if len(doc_L2[-1]) <= len(doc_L[i+1]):
						# previous is smaller or equal, so add to that
						doc_L2[-1] = combine_two_docs(doc_L2[-1], doc_L[i])
						identifer_L2[-1] = combine_two_identifers(identifer_L2[-1], identifer_L[i])
						continue

					else:
						# next is smaller, add to that
						doc_L[i+1] = combine_two_docs(doc_L[i], doc_L[i+1])
						identifer_L[i+1] = combine_two_identifers(identifer_L[i], identifer_L[i+1])
						continue

				except IndexError:
					# jumped to here because next doesn't exist, so just add left
					doc_L2[-1] = combine_two_docs(doc_L2[-1], doc_L[i])
					identifer_L2[-1] = combine_two_identifers(identifer_L2[-1], identifer_L[i])
					continue

			else:
				# nothing already kept, try adding right

				# first, try looking ahead to see whether already at end
				try:
					doc_L[i+1] # check whether next exists

					# if here, next exists, so go ahead and add to right

					doc_L[i+1] = combine_two_docs(doc_L[i], doc_L[i+1])
					identifer_L[i+1] = combine_two_identifers(identifer_L[i], identifer_L[i+1])
					continue

				except IndexError:
					# jumped to here because next doesn't exist, so add left
					doc_L2[-1] = combine_two_docs(doc_L2[-1], doc_L[i])
					identifer_L2[-1] = combine_two_identifers(identifer_L2[-1], identifer_L[i])
					continue

	return doc_L2, identifer_L2

def combine_two_docs(doc_A, doc_B):
	if len(doc_A)==0: return doc_B
	if doc_A[-1] == '_': return doc_A + doc_B
	else: return doc_A + ' ' + doc_B

def combine_two_identifers(identifer_A, identifer_B):

	if identifer_A == '': return identifer_B

	A_stripped = re.sub(u'[\[\]]', '', identifer_A)
	B_stripped = re.sub(u'[\[\]]', '', identifer_B)

	first_part_of_A = A_stripped.split('_')[0]
	last_part_of_B = B_stripped.split('_')[-1]

#
# 	# HERE HERE
#
# 	print "A_stripped", A_stripped
# 	if '^' in A_stripped:
# 		print "'^' in A_stripped"
# 		first_part_of_A = A_stripped[:A_stripped.find('^')] + A_stripped[A_stripped.find('^'):].split('_')[0]
# 	else:
# 		first_part_of_A = A_stripped.split('_')[0]
#
# 	print "B_stripped", B_stripped
# 	if '^' in B_stripped and B_stripped[B_stripped.find('^'):].split('_')[-1].find('_')>0:
# 		print "'^' in B_stripped"
# 		last_part_of_B = B_stripped[B_stripped.find('^'):].split('_')[-1]
# 		print "last_part_of_B", last_part_of_B
# 	else:
# 		last_part_of_B = B_stripped.split('_')[-1]

	identifier_AB = "[%s_%s]" % (first_part_of_A, last_part_of_B)

	# log_id_combo(identifer_A, identifer_B, identifier_AB)
	return identifier_AB

# import logging
# logging.basicConfig(filename='identifier_log.txt',level=logging.DEBUG)
#
# def log_id_combo(A, B, AB):
# 	logging.debug( A.ljust(35) + B.ljust(35) + AB )

#
# """
# Initialization function (1)
# """
#
# def initialize_doc_identifers(section_identifer, doc_identifers):
# 	"""
# 	If doc identifier empty, number with numerical parent section identifer plus integer increment.
# 	"""
#
# 	for i, doc_identifer in enumerate(doc_identifers):
#
# 		old_identifier = doc_identifer # for logging
#
# 		if doc_identifers[i] == ('[]'):
# 			doc_identifers[i] = '[' + section_identifer[1:-1] + '.%d]' % (i+1)
#
# 		logging.debug( old_identifier.ljust(35) + '(init)'.ljust(35) + doc_identifers[i] )
#
# 	return doc_identifers
