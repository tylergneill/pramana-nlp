These files are the direct outcome of training an LDA topic model on the file pramāṇa\_corpus.tsv, using 12 stopwords (iti, na, ca, api, eva, tad, tvāt, tat, hi, ādi, tu, vā), number of topics k = 50, number of iterations = 1000, and all other parameters with default values (i.e., occurrence threshold = 3, seed = 73, alpha = 0.02, eta = 0.02, number of terms shown 25). The modeling took between 60–90 minutes on a 2017 MacBook Air with a 1.8 GHz Intel Core i5 processor and 8 GB RAM running macOS High Sierra 10.13.6.

Once ToPān is installed, simply place the folder "pramana-nlp" into the local directory "ToPan/www/data". Then, with ToPān started (while in ToPān top directory, run R; issue the command "library(shiny)"; then issue the command "runApp()" and switch to working in browser) look on the LDAvis tab for the "pramana-nlp" entry in order to browse.

Most important results (also presented here as cleaned OpenOffice spreadsheets for clarity and for ease of opening):
* pramana-nlp/NBhū\_5,11\_MF15\_K50\_alph002\_eta002\_I1000\_S73\_tab/phi.csv
* pramana-nlp/NBhū\_5,11\_MF15\_K50\_alph002\_eta002\_I1000\_S73\_tab/theta.csv