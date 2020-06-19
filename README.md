# Challenge 2: Tokenization, FDIST, ngrams

Find the n-grams using FDIST function. FDIST and ngrams will give you the laundry list but has a lot of noise, hence the objective is to extract the key frequently occurring ngrams (where n>1 and n<=4) based on n=1 most frequently occurring terms.

This will generate list of 10 most frequent n-grams (n = 2, 3, 4) for each of the 10 most frequent words.

## Prerequisite
* ```ticket_Data.csv``` in ```<project_dir>\data\```

## Changelog
* **19-June-2020**
    - Used object-oriented approach. Modularized all n-gram and fdist operations into ```Ngrams``` class inside ```ngram_toolkit``` module.
    - Added logic for creating list of all the n-grams (n = 1, 2, 3, 4) in separate files. These files are present in the ```<project_dir>\data\``` folder
