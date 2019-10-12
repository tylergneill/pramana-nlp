# pramana-nlp

A corpus of Sanskrit pramāṇa texts ready for use in NLP applications, along with data and results for an experiment in LDA topic modeling. See also corresponding paper to be presented at the [6th ISCLS](https://iscls.github.io).

The numbering of files and folders here suggests a linear order for understanding the corpus-building and modeling processes.

Some data not able to be shared freely here:
Data Sources | 1.1\_text\_original | 2\_data\_prep/1\_text\_metadata | 2\_data\_prep/4\_text\_cleaned | 3.1\_text\_doc\_and\_word\_segmented |
------------ | ------------------- | ------------------------------- | ------------------------------ | ------------------------------------ |
[GRETIL](http://gretil.sub.uni-goettingen.de/gretil.html) | y | y | y | y |
[SARIT](http://sarit.indology.info/) | y | y | y | y |
private collections  | n | y | n | y |

Tools Used:
* Python 2.7
* XSL Transforms: [lxml](https://lxml.de/index.html) library
* Word Segmentation: [Sanskrit Sandhi and Compound Splitter](https://github.com/OliverHellwig/sanskrit/tree/master/papers/2018emnlp), based on [DCS](http://www.sanskrit-linguistics.org/dcs/index.php)
* Transliteration: [Skrutable](https://github.com/tylergneill/Skrutable)
* Topic Modeling: [ToPān](https://github.com/ThomasK81/ToPan), based on R packages [lda](https://cran.r-project.org/web/packages/lda/index.html) and [LDAvis](https://github.com/cpsievert/LDAvis)
* Topic Model Exploration: [Metallō](https://github.com/ThomasK81/Metallo) (local-only fork, please ask for more info)

Micro-Tools Created:
* transform.py - daisy-chain XSL transforms, visualize progress
* (3\_)validate\_text.py - check textual structure (use of brackets) and character content for troublesome patterns, warn about issues
* explore\_topic\_top\_words.py - adjusts topic modeling phi values for lambda relevance L, filters out unwanted words, sets limits on how many words to consider and on how many words to show for each topic
* explore\_topic\_domination\_by\_text.py - shows which topics are dominated by small number of individual texts as determined from identifiers
* format\_doc\_similarity\_table.py - formats document similarity results as table with one column per text as determined from identifiers, optinally prioritizes set of preferred texts

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).