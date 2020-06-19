from pathlib import Path
import csv
import ngram_toolkit as ngtk

inpf_path = Path(Path.cwd(), 'data/ticket_Data.csv')
outf_path = Path(Path.cwd(), 'data/ticket_Data_ngrams.csv')
has_header = True          # Change this to False if the csv file doesn't have a header

fdist_list = [None, None, None, None]          # List containing frequency distributions for 1, 2, 3 and 4-grams

with open(inpf_path, 'r') as inp_csvfile:
    ticket_rdr = csv.reader(inp_csvfile, delimiter=',', quotechar='"')

    if has_header:
        header = next(ticket_rdr)

    for row in ticket_rdr:
        ticket_id, description = row
        row_ngram = ngtk.Ngram(description)

        for i in range(4):
            if not fdist_list[i]:
                fdist_list[i] = row_ngram.get_fdist(i + 1)
            else:
                ng = row_ngram.get_ngrams(i + 1)
                fdist_list[i] = ngtk.Ngram.update_fdist(fdist_list[i], ng)

    # This part creates individual csv files containing all the n-gram and corresponding frequency for n = (1, 2, 3, 4)
    for i in range(4):
        out_fname = 'file_' + str(i + 1) + '-gram.csv'
        out_ngpath = outf_1gram = Path(Path.cwd(), 'data/' + out_fname)

        with open(out_ngpath, 'w', newline='\n', encoding='utf-8') as out_csvfile:
            csvwriter = csv.writer(out_csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['N-gram', 'Frequency'])
            for ng in fdist_list[i]:
                csvwriter.writerow([ng, fdist_list[i][ng]])

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
        for ngram, freq in fdist_list[0].most_common(10):
            word = ngram[0]
            top_2grams = ngtk.Ngram.filter_fdist(fdist_list[1], word).most_common(10)
            top_3grams = ngtk.Ngram.filter_fdist(fdist_list[2], word).most_common(10)
            top_4grams = ngtk.Ngram.filter_fdist(fdist_list[3], word).most_common(10)

            for i in range(10):
                csvwriter.writerow([word,
                                    freq,
                                    top_2grams[i][0],
                                    top_2grams[i][1],
                                    top_3grams[i][0],
                                    top_3grams[i][1],
                                    top_4grams[i][0],
                                    top_4grams[i][1]])
