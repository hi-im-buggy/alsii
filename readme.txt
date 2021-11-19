# Overview

This directory contains the resources used in the following paper: 

"Automatic language identification in code-switched Hindi-English social media text"
Li Nguyen, Christopher Bryant, Sana Kidwai, Theresa Biberauer

Contact: nhbn2@cl.cam.ac.uk (Li Nguyen)

# Data

The Facebook, Twitter and Whatsapp data was all downloaded from: http://amitavadas.com/Code-Mixing.html

This was the data released in the ICON 2016 shared task. See: https://www.aclweb.org/anthology/R15-1033.pdf

We simplified the language tags in each file using the "data/ref/simplify.py" script to create the new "data/ref/*.new" reference files used in evaluation. The equivalent source files are in "data/*.src".


# Resources

The English word list "resources/EN.words.txt" was downloaded from: http://wordlist.aspell.net/

The Hindi transliteration word list "resources/HI.trans.fire2013.txt" was downloaded from: https://web.archive.org/web/20160312153954/http://cse.iitkgp.ac.in/resgrp/cnerg/qa/fire13translit/

The Hindi word list was compiled by Gupta et al. (2012): http://www.lrec-conf.org/proceedings/lrec2012/pdf/365_Paper.pdf

The "resources/word_map.txt" word list was created as part of the present work. 


# Usage

The main annotation script is "process.py". It should be run as follows:

python3 process.py <src_file> [-top_n int] -out <out_file>

Where <src_file> is the input text file in CoNLL-format (1 token per line), and <out_file> is the name of the output file that will be generated. The -top_n flag controls how much of the manually created word list will be used to classify tokens. By default, it uses the whole word list. 


# Automatic Evaluation

The system output can be evaluated using the evaluation script "scorer.py" as follows:

python3 scorer.py -hyp <out_file> -ref <ref_file> [-v]

Where <out_file> is the file produced as output from "process.py", and <ref_file> is the simplified reference file created from the gold standard data (i.e. in "data/ref/"). The optional -v flag controls how much output is printed. By default, the system just prints the confusion matrix and Precision, Recall and F1 for each class and overall.


# Manual Evaluation

Manually annotated errors for the first 500 tokens in each of the Facebook, Twitter and Whatsapp datasets are provided in the "annotations.xlsx" spreadsheet. This spreadsheet also contains the manually annotated tokens (ordered by frequency) that were used to make the manual word list resource. 
