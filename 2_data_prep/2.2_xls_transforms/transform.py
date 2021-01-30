#!/usr/bin/env python
# -*- coding: utf-8 -*-

## transforms xml document (passed in as argument) based on xsl files in respective folder at xsl_template_path, visually summarizes elements before and after

import sys
if len(sys.argv) == 1: print "need argument"; exit()
xml_fn = sys.argv[1]
if xml_fn[-4:] != ".xml": print "need .xml as first argument"; exit()

pause_bw_templates = False
if "--pause" in sys.argv: pause_bw_templates = True

import pdb
stop_for_queries = False
if "--query" in sys.argv: stop_for_queries = True

import lxml.etree as ET
import re, os

def show_structure(xml_tree, do_sort=False):
	# xml_tree is whole ElementTree object, NOT root Element object

	xml_root = xml_tree.getroot() # THIS is the root Element object

	unique_tags = []
	unique_paths = []

	for element in xml_root.iter():

		if element.tag not in unique_tags: unique_tags.append(element.tag)

		path = re.sub('\[[0-9]+\]', '', xml_tree.getpath(element)) # remove unwanted getpath stuff

		if path not in unique_paths: unique_paths.append(path)

 	if do_sort: unique_paths.sort()

	for path in unique_paths: print path.replace('/','\t')

	print
	print "number of unique paths: ", len(unique_paths)
	print "number of unique tags: ", len(unique_tags)

	innermost_tags = unique_tags

	for path in unique_paths:

		curr_path_tags = path.split('/')

		# don't count these against nesting
		if curr_path_tags[-1] in ['lb','pb']: curr_path_tags.pop()

		for tag in innermost_tags:
			if tag in curr_path_tags[:-1]: innermost_tags.remove(tag)

	print "innermost tags (%d): %s" % (len(innermost_tags), innermost_tags)

from HTMLParser import HTMLParser

def clean_attribute_html_entities(text):
	h = HTMLParser()
	pattern = '(&#x.{2,4};)'
	unique_patterns = list(set( re.findall(pattern, text) ))
	for p in unique_patterns:
		text = text.replace(p, h.unescape(p).encode('utf-8'))
	return text

def output_results(xml_tree_transformed):
	out_str = ET.tostring(xml_tree_transformed, encoding='utf-8', pretty_print=True)
	out_str = clean_attribute_html_entities(out_str)
	out_f = open(xml_fn[:-4] + '_transformed.xml', 'w')
	out_f.write(out_str)
	out_f.close()

xml_str = open(xml_fn,'r').read()
xml_root = ET.fromstring(xml_str)

xsl_template_path = 'xsl_templates'
xsl_template_fns = [os.path.join(xsl_template_path,fn) for fn in os.listdir(xsl_template_path) if fn != '.DS_Store']
xsl_template_fns.sort()

xml_tree_transformed = ET.ElementTree(xml_root)
print "Initial structure: "
show_structure(xml_tree_transformed, do_sort=True)
print

all = len(xsl_template_fns)
how_many = all

for xsl_template_fn in xsl_template_fns[0:how_many]:

	xsl_transform = ET.parse(xsl_template_fn)
	Transformer = ET.XSLT(xsl_transform)
	xml_tree_transformed = Transformer(xml_tree_transformed)

	print "Modified structure: "
	show_structure(xml_tree_transformed, do_sort=True)
	print
	output_results(xml_tree_transformed)

	print "Finished with %s" % xsl_template_fn
	print
	if pause_bw_templates:
		print "(press Enter to continue...)"
		raw_input()

	if stop_for_queries:
		print "example query: xml_tree_transformed.xpath('//quote/p')"
		pdb.set_trace()

print "Done"
print