# pramana-nlp

A corpus of Sanskrit pramāṇa texts ready for use in NLP applications, along with data and results for an experiment in LDA topic modeling. See also the corresponding [paper](https://www.aclweb.org/anthology/W19-7505/) presented at the [6th ISCLS](https://iscls.github.io), for which the citable repo snapshot is at: [![DOI](https://zenodo.org/badge/187706215.svg)](https://zenodo.org/badge/latestdoi/187706215)

Update (Jan 2021): I'm currently working on version 2 (= re-cleaned and additional text data, Python 3, new experimentation in similarity calculation). See the above Zenodo link for the archive of version 1.

Repo Overview:

1. text_original: downloaded source files (`.htm` GRETIL, `.xml` SARIT, `.doc` etc. private collections)
2. data_prep: metadata, xls transforms, validation scripts, cleaned texts, segmentation scripts
3. text_doc_and_word_segmented: topic modeling-ready input data, spreadsheet overview thereof
4. lda_topic_modeling: topic modeling inputs and outputs, analysis scripts, results

Overivew of which data could be shared freely here:

Data Source | 1\_text\_original | 2.1\_text\_metadata | 2.4\_text\_cleaned | 3\_text\_doc\_and\_word\_segmented |
------------ | ------------------- | ------------------------------- | ------------------------------ | ------------------------------------ |
[GRETIL](http://gretil.sub.uni-goettingen.de/gretil.html) | y | y | y | y |
[SARIT](http://sarit.indology.info/) | y | y | y | y |
private collections  | ([some](./1_text_original/files_from_private_collections.txt)) | y | ([some](./1_text_original/files_from_private_collections.txt)) | y |

Tools Used:
* Python 2.7 (>> 3.8)
* XSL Transforms: [lxml](https://lxml.de/index.html) library
* Word Segmentation: [Sanskrit Sandhi and Compound Splitter](https://github.com/OliverHellwig/sanskrit/tree/master/papers/2018emnlp), based on [DCS](http://www.sanskrit-linguistics.org/dcs/index.php)
* Transliteration: [skrutable](https://github.com/tylergneill/Skrutable)
* Topic Modeling: [ToPān](https://github.com/ThomasK81/ToPan), based on R packages [lda](https://cran.r-project.org/web/packages/lda/index.html) and [LDAvis](https://github.com/cpsievert/LDAvis)
* Topic Model Exploration: [fork](https://github.com/tylergneill/Metallo_tgn) of [Metallō](https://github.com/ThomasK81/Metallo)

Micro-Tools Created:
* transform.py - daisy-chains XSL transforms, visualize progress
* validate\_text.py - checks textual structure (use of brackets) and character content for troublesome patterns, warns about issues
* explore\_topic\_top\_words.py - adjusts topic modeling phi values for lambda relevance L, filters out unwanted words, sets limits on how many words to consider and on how many words to show for each topic
* explore\_topic\_domination\_by\_text.py - shows which topics are dominated by small number of individual texts as determined from identifiers
* format\_doc\_similarity\_table.py - formats document similarity results as table with one column per text as determined from identifiers, optinally prioritizes set of preferred texts

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).