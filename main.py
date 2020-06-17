import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk.probability import FreqDist
from pathlib import Path
import csv

inpf_path = Path(Path.cwd(), 'data/ticket_Data.csv')
outf_path = Path(Path.cwd(), 'data/ticket_Data_ngrams.csv')
has_header = True          # Change this to False if the csv file doesn't have a header

stop_words = set(stopwords.words('english'))
fdist_word = FreqDist()
fdist_2gram = FreqDist()
fdist_3gram = FreqDist()
fdist_4gram = FreqDist()

with open(inpf_path, 'r') as inp_csvfile:
    ticket_rdr = csv.reader(inp_csvfile, delimiter=',', quotechar='"')

    if has_header:
        header = next(ticket_rdr)

    for row in ticket_rdr:
        ticket_id, description = row
        tokens = nltk.word_tokenize(description)
        tokens = [token.lower() for token in tokens]          # Converting to lowercase
        filtered_tokens = [token for token in tokens if token not in stop_words]          # Removing stopwords

        twograms = ngrams(filtered_tokens, 2)
        threegrams = ngrams(filtered_tokens, 3)
        fourgrams = ngrams(filtered_tokens, 4)

        for token in filtered_tokens:
            fdist_word[token] += 1
        for token in twograms:
            fdist_2gram[token] += 1
        for token in threegrams:
            fdist_3gram[token] += 1
        for token in fourgrams:
            fdist_4gram[token] += 1

    # Removing period '.' and comma ',' from word frequency distribution
    del fdist_word['.']
    del fdist_word[',']

    with open(outf_path, 'w', newline='\n', encoding='utf-8') as out_csvfile:
        csvwriter = csv.writer(out_csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Writing header row
        csvwriter.writerow(['Word',
                            'Frequency',
                            '2-gram',
                            '2-gram freq',
                            '3-gram',
                            '3-gram freq',
                            '4-gram',
                            '4-gram freq'])

        # Processing only for the 10 most common words
        for word, freq in fdist_word.most_common(10):
            temp_fdist2 = FreqDist()
            temp_fdist3 = FreqDist()
            temp_fdist4 = FreqDist()

            # Keeping only 2-grams containing the current word
            for ngram in fdist_2gram:
                if word in ngram:
                    temp_fdist2[ngram] += fdist_2gram[ngram]
            top_2grams = temp_fdist2.most_common(10)

            # Keeping only 3-grams containing the current word
            for ngram in fdist_3gram:
                if word in ngram:
                    temp_fdist3[ngram] += fdist_3gram[ngram]
            top_3grams = temp_fdist3.most_common(10)

            # Keeping only 4-grams containing the current word
            for ngram in fdist_4gram:
                if word in ngram:
                    temp_fdist4[ngram] += fdist_4gram[ngram]
            top_4grams = temp_fdist4.most_common(10)

            for i in range(10):
                csvwriter.writerow([word,
                                    freq,
                                    top_2grams[i][0],
                                    top_2grams[i][1],
                                    top_3grams[i][0],
                                    top_3grams[i][1],
                                    top_4grams[i][0],
                                    top_4grams[i][1]])
