# pramana-nlp

A corpus of Sanskrit pramāṇa texts ready for use in NLP applications, along with data and results for an experiment in LDA topic modeling. See also corresponding paper presented at the [6th ISCLS](https://iscls.github.io).

The numbering of files and folders here suggests a linear order for understanding the corpus-building and modeling processes.

Data Sources:
* [GRETIL](http://gretil.sub.uni-goettingen.de/gretil.html)
* [SARIT](http://sarit.indology.info/)
* private collections

Tools Used:
* Word Analysis: [Sanskrit Sandhi and Compound Splitter](https://github.com/OliverHellwig/sanskrit/tree/master/papers/2018emnlp), based on [DCS](http://www.sanskrit-linguistics.org/dcs/index.php)
* Transliteration: [Skrutable](https://github.com/tylergneill/Skrutable)
* Topic Modeling: [ToPān](https://github.com/ThomasK81/ToPan), based on R packages [lda](https://cran.r-project.org/web/packages/lda/index.html) and [LDAvis](https://github.com/cpsievert/LDAvis)
* Topic Model Exploration: [Metallō](https://github.com/ThomasK81/Metallo) (local branch only, please ask for more info)

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).