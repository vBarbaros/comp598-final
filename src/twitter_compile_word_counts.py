from pathlib import Path

import pandas as pd
import argparse
import os
import sys
import json

ROUND_BY = 2

parentdir = Path(__file__).parents[1]
SPECIAL_CHARS = '()[],-.?!:;&'


def get_stopwords():
    stopwords_txt_file = 'data/results/tf-idf/stopwords.txt'
    stopwords_file = os.path.join(parentdir, stopwords_txt_file)
    stopwords_lst = []
    with open(stopwords_file) as stopf:
        tmp_l = stopf.readlines()
        for i in tmp_l:
            if '#' not in i:
                stopwords_lst.append(i.rstrip())
    return stopwords_lst


def get_tweets_per_label(dataframe, column_name, label_name):
    tmp_tsd = dataframe.loc[dataframe[column_name].str.lower() == label_name]['text']
    return tmp_tsd


def compute_word_frequency_per_label(stopwords_lst, text_dataframe_per_label, all_words_dict):
    label_word_frequency_dict = {}
    for tweet_text in text_dataframe_per_label:
        for sc in SPECIAL_CHARS:
            tweet_text = tweet_text.replace(sc, ' ').lower()
        for word in tweet_text.split():
            word = word.strip()
            if word.isalpha() and word not in stopwords_lst:
                if word in label_word_frequency_dict.keys():
                    label_word_frequency_dict[word] += 1
                else:
                    label_word_frequency_dict[word] = 1

                if word in all_words_dict.keys():
                    all_words_dict[word] += 1
                else:
                    all_words_dict[word] = 1

    return label_word_frequency_dict, all_words_dict


def get_clean_dialogs_dataframe(input_csv_file):
    in_file = os.path.join(parentdir, input_csv_file)
    df = pd.read_csv(in_file)
    return df


def write_to_json(all_ponies_word_frequency_dict, output_json_file):
    output_json_file = os.path.join(parentdir, output_json_file)
    with open(output_json_file, 'w') as fh:
        json.dump(all_ponies_word_frequency_dict, fh, indent=2)


def get_word_frequency_above_threshold(all_labels_dict, all_words_dict, LABEL_TYPE_LIST):
    all_labels_threshold_dict = {}
    for label in LABEL_TYPE_LIST:
        dict_with_threshold = {i: all_labels_dict[label][i] for i in all_labels_dict[label].keys() if
                               all_words_dict[i] >= 5}
        all_labels_threshold_dict[label] = dict_with_threshold
    return all_labels_threshold_dict


def prepare_all_word_frequency_dicts(df, stopwords_lst, column_name, LABEL_TYPE_LIST):
    all_labels_dict = {}
    all_words_dict = {}
    for label in LABEL_TYPE_LIST:
        dialog_dataframe_per_label = get_tweets_per_label(df, column_name, label)
        label_word_frequency_dict, all_words_dict = compute_word_frequency_per_label(stopwords_lst,
                                                                                     dialog_dataframe_per_label,
                                                                                     all_words_dict)
        all_labels_dict[label] = label_word_frequency_dict
    return all_labels_dict, all_words_dict


def get_final_word_frequencies(input_csv_file, column_name, LABEL_TYPE_LIST):
    stopwords_lst = get_stopwords()
    df = get_clean_dialogs_dataframe(input_csv_file)
    all_labels_dict, all_words_dict = prepare_all_word_frequency_dicts(df, stopwords_lst, column_name, LABEL_TYPE_LIST)
    all_labels_threshold_dict = get_word_frequency_above_threshold(all_labels_dict, all_words_dict, LABEL_TYPE_LIST)
    return all_labels_threshold_dict


def main(input_csv_file, output_json_file, column_name, LABEL_TYPE_LIST):
    all_labels_threshold_dict = get_final_word_frequencies(input_csv_file, column_name, LABEL_TYPE_LIST)

    write_to_json(all_labels_threshold_dict, output_json_file)


if __name__ == '__main__':
    # PARAMS_LIST = [
    #     ['data/results/word_frequency_per_filter_type_label_noa.json', 'filter_type', ['gvnmt', 'keyword', 'news']],
    #     ['data/results/word_frequency_per_collected_day_label_noa.json', 'day', ['01_dec', '30_nov', '29_nov']],
    #     ['data/results/word_frequency_per_ca_related_label_noa.json', 'ca_related', ['ca', 'non-ca', 'na']],
    #     ['data/results/word_frequency_per_covid_labels_noa.json', 'labels', ['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'vax-efficiency', 'pandemic-legal']],
    #     ['data/results/word_frequency_per_sentiment_label_noa.json', 'sentiment', ['pos', 'neg', 'neut']]
    # ]

    PARAMS_LIST = [
        ['data/results/word_frequency_per_filter_type_label_notag_noa.json', 'filter_type', ['gvnmt', 'keyword', 'news']],
        ['data/results/word_frequency_per_collected_day_label_notag_noa.json', 'day', ['01_dec', '30_nov', '29_nov']],
        ['data/results/word_frequency_per_ca_related_label_notag_noa.json', 'ca_related', ['ca', 'non-ca', 'na']],
        ['data/results/word_frequency_per_covid_labels_notag_noa.json', 'labels',
         ['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'vax-efficiency', 'pandemic-legal']],
        ['data/results/word_frequency_per_sentiment_label_notag_noa.json', 'sentiment', ['pos', 'neg', 'neut']]
    ]

    # PARAMS_LIST = [
    #     ['data/results/word_frequency_per_filter_type_label.json', 'filter_type', ['gvnmt', 'keyword', 'news']],
    #     ['data/results/word_frequency_per_collected_day_label.json', 'day', ['01_dec', '30_nov', '29_nov']],
    #     ['data/results/word_frequency_per_ca_related_label.json', 'ca_related', ['ca', 'non-ca', 'na']],
    #     ['data/results/word_frequency_per_covid_labels.json', 'labels',
    #      ['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'vax-efficiency', 'pandemic-legal']],
    #     ['data/results/word_frequency_per_sentiment_label.json', 'sentiment', ['pos', 'neg', 'neut']]
    # ]

    for params in PARAMS_LIST:
        input_csv_file = 'data/results/annotated_full_dataset.csv'
        output_json_file = params[0]
        column_name = params[1]
        LABEL_TYPE_LIST = params[2]
        main(input_csv_file, output_json_file, column_name, LABEL_TYPE_LIST)