import math

from twitter_collect import *


def json_to_dict(input_csv_file):
    in_file = os.path.join(parentdir, input_csv_file)
    json_content = None
    with open(in_file, 'r') as fh:
        json_content = json.load(fh)
    return json_content


def compute_tf_idf(all_labels_dict):
    NR_OF_LABELS = len(all_labels_dict.keys())
    all_labels_tf_idf_dict = {}
    for label in all_labels_dict.keys():
        all_labels_tf_idf_dict[label] = {}
        for word in all_labels_dict[label].keys():
            tf = all_labels_dict[label][word]

            nr_of_labels_used_word = 0
            for pony_idf in all_labels_dict.keys():
                if word in all_labels_dict[pony_idf].keys():
                    nr_of_labels_used_word += 1

            idf = math.log(NR_OF_LABELS // nr_of_labels_used_word, 10)

            tf_idf = tf * idf

            all_labels_tf_idf_dict[label][word] = tf_idf
    return all_labels_tf_idf_dict


def get_sorted_tf_idf(all_labels_tf_idf_dict):
    top_n_words_dict = {}
    for label in all_labels_tf_idf_dict.keys():
        sorted_words_tf_idf = sorted(all_labels_tf_idf_dict[label].items(), key=lambda w: w[1], reverse=True)
        top_n_words_dict[label] = sorted_words_tf_idf
    return top_n_words_dict


def get_num_words_list_per_label(num_words, top_n_words_dict):
    final_dict = {}
    for label in top_n_words_dict.keys():
        if num_words <= len(top_n_words_dict[label]):
            # final_dict[label] = [w[0] for w in top_n_words_dict[label]][:num_words]
            final_dict[label] = [w for w in top_n_words_dict[label]][:num_words]
        else:
            # final_dict[label] = [w[0] for w in top_n_words_dict[label]]
            final_dict[label] = [w for w in top_n_words_dict[label]]
    return final_dict


def get_top_n_words_per_label_type_per_tf_idf_score(input_json_file, num_words):
    all_labels_dict = json_to_dict(input_json_file)
    all_labels_tf_idf_dict = compute_tf_idf(all_labels_dict)
    top_n_words_dict = get_sorted_tf_idf(all_labels_tf_idf_dict)
    final_dict = get_num_words_list_per_label(num_words, top_n_words_dict)
    return final_dict


def main(input_json_file, num_words):
    final_dict = get_top_n_words_per_label_type_per_tf_idf_score(input_json_file, num_words)
    # print(json.dumps(final_dict, indent=2))
    print(final_dict.keys())
    for entry in final_dict.keys():
        print(entry, final_dict[entry])



if __name__ == '__main__':
    # NOA files to be processed
    PARAMS_LIST = [
        ['data/results/word_frequency_per_filter_type_label_noa.json', 'filter_type', ['gvnmt', 'keyword', 'news']],
        ['data/results/word_frequency_per_collected_day_label_noa.json', 'day', ['01_dec', '30_nov', '29_nov']],
        ['data/results/word_frequency_per_ca_related_label_noa.json', 'ca_related', ['ca', 'non-ca', 'na']],
        ['data/results/word_frequency_per_covid_labels_noa.json', 'labels', ['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'covid-new-variant', 'pandemic-legal']],
        ['data/results/word_frequency_per_sentiment_label_noa.json', 'sentiment', ['pos', 'neg', 'neut']]
    ]

    # LABEL files to be processed
    # PARAMS_LIST = [
    #     ['data/results/word_frequency_per_filter_type_label.json', 'filter_type', ['gvnmt', 'keyword', 'news']],
    #     ['data/results/word_frequency_per_collected_day_label.json', 'day', ['01_dec', '30_nov', '29_nov']],
    #     ['data/results/word_frequency_per_ca_related_label.json', 'ca_related', ['ca', 'non-ca', 'na']],
    #     ['data/results/word_frequency_per_covid_labels.json', 'labels', ['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'covid-new-variant', 'pandemic-legal']],
    #     ['data/results/word_frequency_per_sentiment_label.json', 'sentiment', ['pos', 'neg', 'neut']]
    # ]


    # NOTAG_NOA files to be processed
    # PARAMS_LIST = [
    #     ['data/results/word_frequency_per_filter_type_label_notag_noa.json', 'filter_type', ['gvnmt', 'keyword', 'news']],
    #     ['data/results/word_frequency_per_collected_day_label_notag_noa.json', 'day', ['01_dec', '30_nov', '29_nov']],
    #     ['data/results/word_frequency_per_ca_related_label_notag_noa.json', 'ca_related', ['ca', 'non-ca', 'na']],
    #     ['data/results/word_frequency_per_covid_labels_notag_noa.json', 'labels',
    #      ['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'covid-new-variant', 'pandemic-legal']],
    #     ['data/results/word_frequency_per_sentiment_label_notag_noa.json', 'sentiment', ['pos', 'neg', 'neut']]
    # ]


    num_words = 10
    for params in PARAMS_LIST:
        input_json_file = params[0]
        main(input_json_file, num_words)
        print('===========================================================')
