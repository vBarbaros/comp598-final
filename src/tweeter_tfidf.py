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
    # PARAMS_LIST = [
    #     ['data/results/word_frequency_per_filter_type_label_noa.json', 'filter_type', ['gvnmt', 'keyword', 'news']],
    #     ['data/results/word_frequency_per_collected_day_label_noa.json', 'day', ['01_dec', '30_nov', '29_nov']],
    #     ['data/results/word_frequency_per_ca_related_label_noa.json', 'ca_related', ['ca', 'non-ca', 'na']],
    #     ['data/results/word_frequency_per_covid_labels_noa.json', 'labels', ['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'vax-efficiency', 'pandemic-legal']],
    #     ['data/results/word_frequency_per_sentiment_label_noa.json', 'sentiment', ['pos', 'neg', 'neut']]
    # ]

    # PRINTOUT
    # dict_keys(['gvnmt', 'keyword', 'news'])
    # gvnmt [('omicron', 0.0), ('variant', 0.0), ('moderna', 0.0), ('vaccine', 0.0), ('dr', 0.0), ('mutations', 0.0), ('idiot', 0.0), ('https', 0.0), ('covaxin', 0.0), ('safest', 0.0)]
    # keyword [('via', 20.993335207665147), ('federal', 20.039092698225822), ('judge', 14.313637641589873), ('biden', 12.882273877430885), ('healthcare', 8.11106133023426), ('ceo', 6.679697566075274), ('house', 6.679697566075274), ('blocks', 6.202576311355612), ('jabs', 5.7254550566359494), ('lamb', 5.248333801916287)]
    # news [('cbc', 3.8169700377572995), ('divide', 2.385606273598312), ('conquer', 2.385606273598312), ('forcing', 0.0), ('vaccine', 0.0), ('normal', 0.0), ('million', 0.0), ('lives', 0.0), ('measures', 0.0), ('passports', 0.0)]
    # ===========================================================
    # dict_keys(['01_dec', '30_nov', '29_nov'])
    # 01_dec [('lamb', 5.248333801916287), ('marcus', 3.8169700377572995), ('im', 3.8169700377572995), ('christian', 3.339848783037637), ('pay', 2.385606273598312), ('shutdown', 2.385606273598312), ('life', 0.0), ('accept', 0.0), ('vaccine', 0.0), ('service', 0.0)]
    # 30_nov [('eligible', 3.339848783037637), ('omnicron', 2.385606273598312), ('divide', 2.385606273598312), ('conquer', 2.385606273598312), ('love', 0.0), ('living', 0.0), ('life', 0.0), ('normal', 0.0), ('mask', 0.0), ('vaccine', 0.0)]
    # 29_nov [('action', 2.8627275283179747), ('parents', 0.0), ('covid', 0.0), ('decision', 0.0), ('vaccine', 0.0), ('friends', 0.0), ('shot', 0.0), ('people', 0.0), ('feel', 0.0), ('https', 0.0)]
    # ===========================================================
    # dict_keys(['ca', 'non-ca', 'na'])
    # ca [('cbc', 3.8169700377572995), ('ontario', 2.8627275283179747), ('lol', 2.8627275283179747), ('rna', 2.385606273598312), ('seriously', 2.385606273598312), ('doesnt', 2.385606273598312), ('cnbc', 0.0), ('study', 0.0), ('science', 0.0), ('immunity', 0.0)]
    # non-ca [('african', 4.294091292476962), ('missouri', 3.8169700377572995), ('accept', 2.385606273598312), ('york', 2.385606273598312), ('india', 2.385606273598312), ('trump', 2.385606273598312), ('jim', 2.385606273598312), ('civil', 2.385606273598312), ('halts', 2.385606273598312), ('waiver', 2.385606273598312)]
    # na [('appointment', 3.8169700377572995), ('friends', 3.339848783037637), ('hey', 3.339848783037637), ('post', 2.8627275283179747), ('family', 2.385606273598312), ('season', 2.385606273598312), ('centres', 2.385606273598312), ('god', 0.0), ('vaccine', 0.0), ('effect', 0.0)]
    # ===========================================================
    # dict_keys(['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'pandemic-legal'])
    # covid-controversy [('christian', 4.214419939295736), ('patience', 3.6123599479677737), ('died', 3.3113299523037925), ('lamb', 3.0102999566398116), ('advice', 3.0102999566398116), ('die', 3.0102999566398116), ('common', 3.0102999566398116), ('divide', 3.0102999566398116), ('conquer', 3.0102999566398116), ('kill', 2.408239965311849)]
    # vax-efficiency [('ceo', 6.020599913279623), ('lt', 6.020599913279623), ('gt', 3.0102999566398116), ('adverse', 2.7092699609758304), ('severe', 2.408239965311849), ('leading', 2.408239965311849), ('reactions', 2.408239965311849), ('hospitalized', 2.408239965311849), ('symptoms', 1.8061799739838869), ('severity', 1.8061799739838869)]
    # pandemic-logistics [('johnson', 6.020599913279623), ('appointment', 4.816479930623698), ('clinics', 4.816479930623698), ('african', 4.816479930623698), ('dec', 4.214419939295736), ('olds', 4.214419939295736), ('aged', 3.6123599479677737), ('add', 3.6123599479677737), ('businesses', 3.6123599479677737), ('clinic', 3.3113299523037925)]
    # pandemic-legal [('judge', 8.729869874255453), ('blocks', 7.82677988726351), ('missouri', 4.816479930623698), ('injunction', 4.214419939295736), ('blocked', 3.6123599479677737), ('block', 3.0102999566398116), ('halts', 3.0102999566398116), ('house', 2.107209969647868), ('unconstitutional', 1.8061799739838869), ('breaking', 1.5051499783199058)]
    # ===========================================================
    # dict_keys(['pos', 'neg', 'neut'])
    # pos [('county', 2.8627275283179747), ('service', 2.385606273598312), ('life', 0.0), ('accept', 0.0), ('vaccine', 0.0), ('mandatory', 0.0), ('choice', 0.0), ('god', 0.0), ('effect', 0.0), ('site', 0.0)]
    # neg [('blood', 4.294091292476962), ('power', 3.8169700377572995), ('causing', 2.8627275283179747), ('explain', 2.8627275283179747), ('article', 2.8627275283179747), ('shutdown', 2.385606273598312), ('civil', 2.385606273598312), ('guys', 2.385606273598312), ('past', 2.385606273598312), ('common', 2.385606273598312)]
    # neut [('class', 2.385606273598312), ('covid', 0.0), ('vaccination', 0.0), ('centre', 0.0), ('people', 0.0), ('vaccinated', 0.0), ('weeks', 0.0), ('read', 0.0), ('gt', 0.0), ('https', 0.0)]
    # ===========================================================

    # PARAMS_LIST = [
    #     ['data/results/word_frequency_per_filter_type_label.json', 'filter_type', ['gvnmt', 'keyword', 'news']],
    #     ['data/results/word_frequency_per_collected_day_label.json', 'day', ['01_dec', '30_nov', '29_nov']],
    #     ['data/results/word_frequency_per_ca_related_label.json', 'ca_related', ['ca', 'non-ca', 'na']],
    #     ['data/results/word_frequency_per_covid_labels.json', 'labels', ['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'vax-efficiency', 'pandemic-legal']],
    #     ['data/results/word_frequency_per_sentiment_label.json', 'sentiment', ['pos', 'neg', 'neut']]
    # ]

    # PRINTOUT
    # dict_keys(['gvnmt', 'keyword', 'news'])
    # gvnmt [('govcanhealth', 3.339848783037637), ('ruralsasknews', 2.8627275283179747), ('jkenney', 2.385606273598312), ('celliottability', 2.385606273598312), ('kyliespeak', 2.385606273598312), ('justintrudeau', 0.0), ('omicron', 0.0), ('variant', 0.0), ('moderna', 0.0), ('vaccine', 0.0)]
    # keyword [('via', 20.993335207665147), ('federal', 20.039092698225822), ('judge', 14.313637641589873), ('biden', 12.882273877430885), ('healthcare', 8.11106133023426), ('ceo', 6.679697566075274), ('house', 6.679697566075274), ('blocks', 6.202576311355612), ('jabs', 5.7254550566359494), ('lamb', 5.248333801916287)]
    # news [('nationalpost', 12.405152622711224), ('cbcalerts', 11.928031367991561), ('globeandmail', 11.928031367991561), ('cbc', 3.8169700377572995), ('picardonhealth', 2.385606273598312), ('murcut', 2.385606273598312), ('divide', 2.385606273598312), ('conquer', 2.385606273598312), ('forcing', 0.0), ('vaccine', 0.0)]
    # ===========================================================
    # dict_keys(['01_dec', '30_nov', '29_nov'])
    # 01_dec [('lamb', 5.248333801916287), ('marcus', 3.8169700377572995), ('im', 3.8169700377572995), ('christian', 3.339848783037637), ('ruralsasknews', 2.8627275283179747), ('pay', 2.385606273598312), ('shutdown', 2.385606273598312), ('life', 0.0), ('accept', 0.0), ('vaccine', 0.0)]
    # 30_nov [('eligible', 3.339848783037637), ('change', 2.385606273598312), ('omnicron', 2.385606273598312), ('murcut', 2.385606273598312), ('divide', 2.385606273598312), ('conquer', 2.385606273598312), ('love', 0.0), ('living', 0.0), ('life', 0.0), ('normal', 0.0)]
    # 29_nov [('action', 2.8627275283179747), ('parents', 0.0), ('covid', 0.0), ('decision', 0.0), ('vaccine', 0.0), ('friends', 0.0), ('shot', 0.0), ('people', 0.0), ('feel', 0.0), ('https', 0.0)]
    # ===========================================================
    # dict_keys(['ca', 'non-ca', 'na'])
    # ca [('cbc', 3.8169700377572995), ('ontario', 2.8627275283179747), ('ruralsasknews', 2.8627275283179747), ('lol', 2.8627275283179747), ('rna', 2.385606273598312), ('jkenney', 2.385606273598312), ('seriously', 2.385606273598312), ('doesnt', 2.385606273598312), ('kyliespeak', 2.385606273598312), ('picardonhealth', 2.385606273598312)]
    # non-ca [('african', 4.294091292476962), ('missouri', 3.8169700377572995), ('accept', 2.385606273598312), ('york', 2.385606273598312), ('india', 2.385606273598312), ('trump', 2.385606273598312), ('jim', 2.385606273598312), ('civil', 2.385606273598312), ('halts', 2.385606273598312), ('waiver', 2.385606273598312)]
    # na [('appointment', 3.8169700377572995), ('friends', 3.339848783037637), ('hey', 3.339848783037637), ('post', 2.8627275283179747), ('family', 2.385606273598312), ('season', 2.385606273598312), ('centres', 2.385606273598312), ('god', 0.0), ('vaccine', 0.0), ('effect', 0.0)]
    # ===========================================================
    # dict_keys(['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'pandemic-legal'])
    # covid-controversy [('christian', 4.214419939295736), ('patience', 3.6123599479677737), ('died', 3.3113299523037925), ('lamb', 3.0102999566398116), ('advice', 3.0102999566398116), ('die', 3.0102999566398116), ('common', 3.0102999566398116), ('divide', 3.0102999566398116), ('conquer', 3.0102999566398116), ('kill', 2.408239965311849)]
    # vax-efficiency [('ceo', 6.020599913279623), ('lt', 6.020599913279623), ('gt', 3.0102999566398116), ('adverse', 2.7092699609758304), ('severe', 2.408239965311849), ('leading', 2.408239965311849), ('reactions', 2.408239965311849), ('hospitalized', 2.408239965311849), ('symptoms', 1.8061799739838869), ('severity', 1.8061799739838869)]
    # pandemic-logistics [('johnson', 6.020599913279623), ('appointment', 4.816479930623698), ('clinics', 4.816479930623698), ('african', 4.816479930623698), ('dec', 4.214419939295736), ('olds', 4.214419939295736), ('aged', 3.6123599479677737), ('add', 3.6123599479677737), ('businesses', 3.6123599479677737), ('clinic', 3.3113299523037925)]
    # pandemic-legal [('judge', 8.729869874255453), ('blocks', 7.82677988726351), ('missouri', 4.816479930623698), ('injunction', 4.214419939295736), ('blocked', 3.6123599479677737), ('block', 3.0102999566398116), ('halts', 3.0102999566398116), ('house', 2.107209969647868), ('unconstitutional', 1.8061799739838869), ('breaking', 1.5051499783199058)]
    # ===========================================================
    # dict_keys(['pos', 'neg', 'neut'])
    # pos [('county', 2.8627275283179747), ('service', 2.385606273598312), ('life', 0.0), ('accept', 0.0), ('vaccine', 0.0), ('mandatory', 0.0), ('choice', 0.0), ('god', 0.0), ('effect', 0.0), ('site', 0.0)]
    # neg [('blood', 4.294091292476962), ('power', 3.8169700377572995), ('causing', 2.8627275283179747), ('joebiden', 2.8627275283179747), ('explain', 2.8627275283179747), ('article', 2.8627275283179747), ('shutdown', 2.385606273598312), ('civil', 2.385606273598312), ('guys', 2.385606273598312), ('past', 2.385606273598312)]
    # neut [('class', 2.385606273598312), ('covid', 0.0), ('vaccination', 0.0), ('centre', 0.0), ('people', 0.0), ('vaccinated', 0.0), ('weeks', 0.0), ('read', 0.0), ('gt', 0.0), ('https', 0.0)]
    # ===========================================================


    PARAMS_LIST = [
        ['data/results/word_frequency_per_filter_type_label_notag_noa.json', 'filter_type', ['gvnmt', 'keyword', 'news']],
        ['data/results/word_frequency_per_collected_day_label_notag_noa.json', 'day', ['01_dec', '30_nov', '29_nov']],
        ['data/results/word_frequency_per_ca_related_label_notag_noa.json', 'ca_related', ['ca', 'non-ca', 'na']],
        ['data/results/word_frequency_per_covid_labels_notag_noa.json', 'labels',
         ['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'vax-efficiency', 'pandemic-legal']],
        ['data/results/word_frequency_per_sentiment_label_notag_noa.json', 'sentiment', ['pos', 'neg', 'neut']]
    ]

    # PRINTOUT
    # dict_keys(['gvnmt', 'keyword', 'news'])
    # gvnmt [('omicron', 0.0), ('variant', 0.0), ('moderna', 0.0), ('vaccine', 0.0), ('dr', 0.0), ('mutations', 0.0), ('idiot', 0.0), ('https', 0.0), ('covaxin', 0.0), ('safest', 0.0)]
    # keyword [('via', 20.993335207665147), ('federal', 20.039092698225822), ('judge', 14.313637641589873), ('biden', 12.882273877430885), ('healthcare', 6.679697566075274), ('ceo', 6.679697566075274), ('house', 6.679697566075274), ('blocks', 6.202576311355612), ('jabs', 5.7254550566359494), ('lamb', 5.248333801916287)]
    # news [('cbc', 3.8169700377572995), ('divide', 2.385606273598312), ('conquer', 2.385606273598312), ('forcing', 0.0), ('vaccine', 0.0), ('normal', 0.0), ('million', 0.0), ('lives', 0.0), ('measures', 0.0), ('passports', 0.0)]
    # ===========================================================
    # dict_keys(['01_dec', '30_nov', '29_nov'])
    # 01_dec [('lamb', 5.248333801916287), ('marcus', 3.8169700377572995), ('im', 3.8169700377572995), ('christian', 3.339848783037637), ('pay', 2.385606273598312), ('shutdown', 2.385606273598312), ('life', 0.0), ('accept', 0.0), ('vaccine', 0.0), ('service', 0.0)]
    # 30_nov [('eligible', 3.339848783037637), ('divide', 2.385606273598312), ('conquer', 2.385606273598312), ('love', 0.0), ('living', 0.0), ('life', 0.0), ('normal', 0.0), ('mask', 0.0), ('vaccine', 0.0), ('https', 0.0)]
    # 29_nov [('action', 2.8627275283179747), ('parents', 0.0), ('covid', 0.0), ('decision', 0.0), ('vaccine', 0.0), ('friends', 0.0), ('shot', 0.0), ('people', 0.0), ('feel', 0.0), ('https', 0.0)]
    # ===========================================================
    # dict_keys(['ca', 'non-ca', 'na'])
    # ca [('cbc', 3.8169700377572995), ('lol', 2.8627275283179747), ('rna', 2.385606273598312), ('ontario', 2.385606273598312), ('seriously', 2.385606273598312), ('doesnt', 2.385606273598312), ('cnbc', 0.0), ('study', 0.0), ('science', 0.0), ('immunity', 0.0)]
    # non-ca [('african', 4.294091292476962), ('missouri', 3.339848783037637), ('accept', 2.385606273598312), ('york', 2.385606273598312), ('trump', 2.385606273598312), ('jim', 2.385606273598312), ('civil', 2.385606273598312), ('halts', 2.385606273598312), ('waiver', 2.385606273598312), ('life', 0.0)]
    # na [('appointment', 3.8169700377572995), ('friends', 3.339848783037637), ('hey', 3.339848783037637), ('post', 2.8627275283179747), ('family', 2.385606273598312), ('season', 2.385606273598312), ('centres', 2.385606273598312), ('god', 0.0), ('vaccine', 0.0), ('effect', 0.0)]
    # ===========================================================
    # dict_keys(['covid-controversy', 'vax-efficiency', 'pandemic-logistics', 'pandemic-legal'])
    # covid-controversy [('christian', 4.214419939295736), ('patience', 3.6123599479677737), ('died', 3.3113299523037925), ('lamb', 3.0102999566398116), ('advice', 3.0102999566398116), ('die', 3.0102999566398116), ('common', 3.0102999566398116), ('divide', 3.0102999566398116), ('conquer', 3.0102999566398116), ('kill', 2.408239965311849)]
    # vax-efficiency [('ceo', 6.020599913279623), ('lt', 6.020599913279623), ('gt', 3.0102999566398116), ('adverse', 2.7092699609758304), ('severe', 2.408239965311849), ('leading', 2.408239965311849), ('reactions', 2.408239965311849), ('hospitalized', 2.408239965311849), ('symptoms', 1.8061799739838869), ('severity', 1.8061799739838869)]
    # pandemic-logistics [('johnson', 6.020599913279623), ('appointment', 4.816479930623698), ('clinics', 4.816479930623698), ('african', 4.816479930623698), ('dec', 4.214419939295736), ('olds', 4.214419939295736), ('aged', 3.6123599479677737), ('add', 3.6123599479677737), ('businesses', 3.6123599479677737), ('clinic', 3.3113299523037925)]
    # pandemic-legal [('judge', 8.729869874255453), ('blocks', 7.82677988726351), ('injunction', 4.214419939295736), ('missouri', 4.214419939295736), ('blocked', 3.6123599479677737), ('block', 3.0102999566398116), ('halts', 3.0102999566398116), ('house', 2.107209969647868), ('unconstitutional', 1.8061799739838869), ('breaking', 1.5051499783199058)]
    # ===========================================================
    # dict_keys(['pos', 'neg', 'neut'])
    # pos [('county', 2.8627275283179747), ('service', 2.385606273598312), ('life', 0.0), ('accept', 0.0), ('vaccine', 0.0), ('mandatory', 0.0), ('choice', 0.0), ('god', 0.0), ('effect', 0.0), ('site', 0.0)]
    # neg [('blood', 4.294091292476962), ('power', 3.8169700377572995), ('causing', 2.8627275283179747), ('explain', 2.8627275283179747), ('article', 2.8627275283179747), ('shutdown', 2.385606273598312), ('civil', 2.385606273598312), ('guys', 2.385606273598312), ('past', 2.385606273598312), ('common', 2.385606273598312)]
    # neut [('class', 2.385606273598312), ('covid', 0.0), ('vaccination', 0.0), ('centre', 0.0), ('people', 0.0), ('vaccinated', 0.0), ('weeks', 0.0), ('read', 0.0), ('gt', 0.0), ('https', 0.0)]
    # ===========================================================

    num_words = 10
    for params in PARAMS_LIST:
        input_json_file = params[0]
        main(input_json_file, num_words)
        print('===========================================================')
