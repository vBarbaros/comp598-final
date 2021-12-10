from twitter_collect import *

paths = [
    'data/annotated_final/dec_01_twitter_dump_by_keywords_final.csv',
    'data/annotated_final/nov_30_twitter_dump_by_keywords_final.csv',
    'data/annotated_final/nov_29_twitter_dump_by_keywords_final.csv',
    'data/annotated_final/dec_01_twitter_dump_replies_gvmnt_only_final.csv',
    'data/annotated_final/nov_30_twitter_dump_replies_gvmnt_only_final.csv',
    'data/annotated_final/nov_29_twitter_dump_replies_gvmnt_only_final.csv',
    'data/annotated_final/dec_01_twitter_dump_replies_news_channels_only_final.csv',
    'data/annotated_final/nov_30_twitter_dump_replies_news_channels_only_final.csv',
    'data/annotated_final/nov_29_twitter_dump_replies_news_channels_only_final.csv',
]

ALL_TWEETS_CSV = 'data/results/annotated_full_dataset.csv'


def generate_unique_csv():
    dfs_all = []
    for csv_file in paths:
        df = read_from_csv_collected_tweets(csv_file)
        dfs_all.append(df)
    dfs_concat_all = pd.concat(dfs_all, ignore_index=True)
    append_to_csv(dfs_concat_all, ALL_TWEETS_CSV)


def generate_stats_per_label():
    df_pos_only = df.loc[df['sentiment'] == 'pos'].copy().shape[0]
    df_neg_only = df.loc[df['sentiment'] == 'neg'].copy().shape[0]
    df_neut_only = df.loc[df['sentiment'] == 'neut'].copy().shape[0]

    df_controversy_only = df.loc[df['labels'] == 'covid-controversy'].copy().shape[0]
    df_new_variant_only = df.loc[df['labels'] == 'covid-new-variant'].copy().shape[0]
    df_legal_only = df.loc[df['labels'] == 'pandemic-legal'].copy().shape[0]
    df_logistics_only = df.loc[df['labels'] == 'pandemic-logistics'].copy().shape[0]
    df_efficiency_only = df.loc[df['labels'] == 'vax-efficiency'].copy().shape[0]

    df_ca_only = df.loc[df['ca_related'] == 'ca'].copy().shape[0]
    df_non_ca_only = df.loc[df['ca_related'] == 'non-ca'].copy().shape[0]
    df_na_only = df.loc[df['ca_related'] == 'na'].copy().shape[0]

    df_01_dec_only = df.loc[df['day'] == '01_dec'].copy().shape[0]
    df_30_nov_only = df.loc[df['day'] == '30_nov'].copy().shape[0]
    df_29_nov_only = df.loc[df['day'] == '29_nov'].copy().shape[0]

    df_gvnmt_only = df.loc[df['filter_type'] == 'gvnmt'].copy().shape[0]
    df_keyword_only = df.loc[df['filter_type'] == 'keyword'].copy().shape[0]
    df_news_only = df.loc[df['filter_type'] == 'news'].copy().shape[0]

    dict_stats_per_label = {
        'sentiment': {
            'pos': [df_pos_only, "{:.4f}".format(df_pos_only / float(df_pos_only + df_neg_only + df_neut_only) * 100)],
            'neg': [df_neg_only, "{:.4f}".format(df_neg_only / float(df_pos_only + df_neg_only + df_neut_only) * 100)],
            'neut': [df_neut_only, "{:.4f}".format(df_neut_only / float(df_pos_only + df_neg_only + df_neut_only) * 100)],
            'sum': df_pos_only + df_neg_only + df_neut_only
        },
        'labels': {
            'covid-controversy': [df_controversy_only, "{:.4f}".format(df_controversy_only / float(
                df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only) * 100)],
            'covid-new-variant': [df_new_variant_only, "{:.4f}".format(df_new_variant_only / float(
                df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only) * 100)],
            'pandemic-legal': [df_legal_only, "{:.4f}".format(
                df_legal_only / float(df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only) * 100)],
            'covid-logistics': [df_logistics_only, "{:.4f}".format(
                df_logistics_only / float(df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only) * 100)],
            'vax-efficiency': [df_efficiency_only, "{:.4f}".format(df_efficiency_only / float(
                df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only) * 100)],
            'sum': df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only
        },
        'ca-related': {
            'ca': [df_ca_only, "{:.4f}".format(df_ca_only / float(df_ca_only + df_non_ca_only + df_na_only) * 100)],
            'non-ca': [df_non_ca_only, "{:.4f}".format(df_non_ca_only / float(df_ca_only + df_non_ca_only + df_na_only) * 100)],
            'na': [df_na_only, "{:.4f}".format(df_na_only / float(df_ca_only + df_non_ca_only + df_na_only) * 100)],
            'sum': df_ca_only + df_non_ca_only + df_na_only
        },
        'day': {
            '01-dec': [df_01_dec_only, "{:.4f}".format(df_01_dec_only / float(df_01_dec_only + df_30_nov_only + df_29_nov_only) * 100)],
            '30-nov': [df_30_nov_only, "{:.4f}".format(df_30_nov_only / float(df_01_dec_only + df_30_nov_only + df_29_nov_only) * 100)],
            '29-nov': [df_29_nov_only, "{:.4f}".format(df_29_nov_only / float(df_01_dec_only + df_30_nov_only + df_29_nov_only) * 100)],
            'sum': df_01_dec_only + df_30_nov_only + df_29_nov_only
        },
        'filter-type': {
            'gvnmt': [df_gvnmt_only, "{:.4f}".format(df_gvnmt_only / float(df_gvnmt_only + df_keyword_only + df_news_only) * 100)],
            'keyword': [df_keyword_only, "{:.4f}".format(df_keyword_only / float(df_gvnmt_only + df_keyword_only + df_news_only) * 100)],
            'news': [df_news_only, "{:.4f}".format(df_news_only / float(df_gvnmt_only + df_keyword_only + df_news_only) * 100)],
            'sum': df_gvnmt_only + df_keyword_only + df_news_only
        }
    }
    write_to_json(dict_stats_per_label, 'data/results/stats_overall_separate_label_type.json', write_param='w')


def generate_stats_per_day():
    df_01_dec_gvnmt = df.loc[((df['day'] == '01_dec') & (df['filter_type'] == 'gvnmt'))].copy().shape[0]
    df_01_dec_keyword = df.loc[((df['day'] == '01_dec') & (df['filter_type'] == 'keyword'))].copy().shape[0]
    df_01_dec_news = df.loc[((df['day'] == '01_dec') & (df['filter_type'] == 'news'))].copy().shape[0]

    df_01_dec_pos = df.loc[((df['day'] == '01_dec') & (df['sentiment'] == 'pos'))].copy().shape[0]
    df_01_dec_neg = df.loc[((df['day'] == '01_dec') & (df['sentiment'] == 'neg'))].copy().shape[0]
    df_01_dec_neut = df.loc[((df['day'] == '01_dec') & (df['sentiment'] == 'neut'))].copy().shape[0]

    df_01_dec_controversy = df.loc[((df['day'] == '01_dec') & (df['labels'] == 'covid-controversy'))].copy().shape[0]
    df_01_dec_new_variant = df.loc[((df['day'] == '01_dec') & (df['labels'] == 'covid-new-variant'))].copy().shape[0]
    df_01_dec_legal = df.loc[((df['day'] == '01_dec') & (df['labels'] == 'pandemic-legal'))].copy().shape[0]
    df_01_dec_logistics = df.loc[((df['day'] == '01_dec') & (df['labels'] == 'pandemic-logistics'))].copy().shape[0]
    df_01_dec_efficiency = df.loc[((df['day'] == '01_dec') & (df['labels'] == 'vax-efficiency'))].copy().shape[0]

    df_01_dec_ca = df.loc[((df['day'] == '01_dec') & (df['ca_related'] == 'ca'))].copy().shape[0]
    df_01_dec_non_ca = df.loc[((df['day'] == '01_dec') & (df['ca_related'] == 'non-ca'))].copy().shape[0]
    df_01_dec_na = df.loc[((df['day'] == '01_dec') & (df['ca_related'] == 'na'))].copy().shape[0]

    df_30_nov_gvnmt = df.loc[((df['day'] == '30_nov') & (df['filter_type'] == 'gvnmt'))].copy().shape[0]
    df_30_nov_keyword = df.loc[((df['day'] == '30_nov') & (df['filter_type'] == 'keyword'))].copy().shape[0]
    df_30_nov_news = df.loc[((df['day'] == '30_nov') & (df['filter_type'] == 'news'))].copy().shape[0]

    df_30_nov_pos = df.loc[((df['day'] == '30_nov') & (df['sentiment'] == 'pos'))].copy().shape[0]
    df_30_nov_neg = df.loc[((df['day'] == '30_nov') & (df['sentiment'] == 'neg'))].copy().shape[0]
    df_30_nov_neut = df.loc[((df['day'] == '30_nov') & (df['sentiment'] == 'neut'))].copy().shape[0]

    df_30_nov_controversy = df.loc[((df['day'] == '30_nov') & (df['labels'] == 'covid-controversy'))].copy().shape[0]
    df_30_nov_new_variant = df.loc[((df['day'] == '30_nov') & (df['labels'] == 'covid-new-variant'))].copy().shape[0]
    df_30_nov_legal = df.loc[((df['day'] == '30_nov') & (df['labels'] == 'pandemic-legal'))].copy().shape[0]
    df_30_nov_logistics = df.loc[((df['day'] == '30_nov') & (df['labels'] == 'pandemic-logistics'))].copy().shape[0]
    df_30_nov_efficiency = df.loc[((df['day'] == '30_nov') & (df['labels'] == 'vax-efficiency'))].copy().shape[0]

    df_30_nov_ca = df.loc[((df['day'] == '30_nov') & (df['ca_related'] == 'ca'))].copy().shape[0]
    df_30_nov_non_ca = df.loc[((df['day'] == '30_nov') & (df['ca_related'] == 'non-ca'))].copy().shape[0]
    df_30_nov_na = df.loc[((df['day'] == '30_nov') & (df['ca_related'] == 'na'))].copy().shape[0]

    df_29_nov_gvnmt = df.loc[((df['day'] == '29_nov') & (df['filter_type'] == 'gvnmt'))].copy().shape[0]
    df_29_nov_keyword = df.loc[((df['day'] == '29_nov') & (df['filter_type'] == 'keyword'))].copy().shape[0]
    df_29_nov_news = df.loc[((df['day'] == '29_nov') & (df['filter_type'] == 'news'))].copy().shape[0]

    df_29_nov_pos = df.loc[((df['day'] == '29_nov') & (df['sentiment'] == 'pos'))].copy().shape[0]
    df_29_nov_neg = df.loc[((df['day'] == '29_nov') & (df['sentiment'] == 'neg'))].copy().shape[0]
    df_29_nov_neut = df.loc[((df['day'] == '29_nov') & (df['sentiment'] == 'neut'))].copy().shape[0]

    df_29_nov_controversy = df.loc[((df['day'] == '29_nov') & (df['labels'] == 'covid-controversy'))].copy().shape[0]
    df_29_nov_new_variant = df.loc[((df['day'] == '29_nov') & (df['labels'] == 'covid-new-variant'))].copy().shape[0]
    df_29_nov_legal = df.loc[((df['day'] == '29_nov') & (df['labels'] == 'pandemic-legal'))].copy().shape[0]
    df_29_nov_logistics = df.loc[((df['day'] == '29_nov') & (df['labels'] == 'pandemic-logistics'))].copy().shape[0]
    df_29_nov_efficiency = df.loc[((df['day'] == '29_nov') & (df['labels'] == 'vax-efficiency'))].copy().shape[0]

    df_29_nov_ca = df.loc[((df['day'] == '29_nov') & (df['ca_related'] == 'ca'))].copy().shape[0]
    df_29_nov_non_ca = df.loc[((df['day'] == '29_nov') & (df['ca_related'] == 'non-ca'))].copy().shape[0]
    df_29_nov_na = df.loc[((df['day'] == '29_nov') & (df['ca_related'] == 'na'))].copy().shape[0]

    dict_stats_per_day = {
        '29_nov': {
            'filter-type': {
                'gvnmt': [df_29_nov_gvnmt, "{:.4f}".format(df_29_nov_news / float(df_29_nov_gvnmt + df_29_nov_keyword + df_29_nov_news) * 100)],
                'keyword': [df_29_nov_keyword,
                            "{:.4f}".format(df_29_nov_keyword / float(df_29_nov_gvnmt + df_29_nov_keyword + df_29_nov_news) * 100)],
                'news': [df_29_nov_news, "{:.4f}".format(df_29_nov_news / float(df_29_nov_gvnmt + df_29_nov_keyword + df_29_nov_news) * 100)],
                'sum': df_29_nov_gvnmt + df_29_nov_keyword + df_29_nov_news
            },
            'ca-related': {
                'ca': [df_29_nov_ca, "{:.4f}".format(df_29_nov_ca / float(df_29_nov_ca + df_29_nov_non_ca + df_29_nov_na) * 100)],
                'non-ca': [df_29_nov_non_ca, "{:.4f}".format(df_29_nov_non_ca / float(df_29_nov_ca + df_29_nov_non_ca + df_29_nov_na) * 100)],
                'na': [df_29_nov_na, "{:.4f}".format(df_29_nov_na / float(df_29_nov_ca + df_29_nov_non_ca + df_29_nov_na) * 100)],
                'sum': df_29_nov_ca + df_29_nov_non_ca + df_29_nov_na
            },
            'sentiment': {
                'pos': [df_29_nov_pos, "{:.4f}".format(df_29_nov_pos / float(df_29_nov_pos + df_29_nov_neg + df_29_nov_neut) * 100)],
                'neg': [df_29_nov_neg, "{:.4f}".format(df_29_nov_neg / float(df_29_nov_pos + df_29_nov_neg + df_29_nov_neut) * 100)],
                'neut': [df_29_nov_neut, "{:.4f}".format(df_29_nov_neut / float(df_29_nov_pos + df_29_nov_neg + df_29_nov_neut) * 100)],
                'sum': df_29_nov_pos + df_29_nov_neg + df_29_nov_neut
            },
            'labels': {
                'covid-controversy': [df_29_nov_controversy, "{:.4f}".format(df_29_nov_controversy / float(
                    df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency) * 100)],
                'covid-new-variant': [df_29_nov_new_variant, "{:.4f}".format(df_29_nov_new_variant / float(
                    df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency) * 100)],
                'pandemic-legal': [df_29_nov_legal, "{:.4f}".format(df_29_nov_legal / float(
                    df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency) * 100)],
                'pandemic-logistics': [df_29_nov_logistics, "{:.4f}".format(df_29_nov_logistics / float(
                    df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency) * 100)],
                'vax-efficiency': [df_29_nov_efficiency, "{:.4f}".format(df_29_nov_efficiency / float(
                    df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency) * 100)],
                'sum': df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency
            }
        },
        '30_nov': {
            'filter-type': {
                'gvnmt': [df_30_nov_gvnmt, "{:.4f}".format(df_30_nov_gvnmt / float(df_30_nov_gvnmt + df_30_nov_keyword + df_30_nov_news) * 100)],
                'keyword': [df_30_nov_keyword,
                            "{:.4f}".format(df_30_nov_keyword / float(df_30_nov_gvnmt + df_30_nov_keyword + df_30_nov_news) * 100)],
                'news': [df_30_nov_news, "{:.4f}".format(df_30_nov_news / float(df_30_nov_gvnmt + df_30_nov_keyword + df_30_nov_news) * 100)],
                'sum': df_30_nov_gvnmt + df_30_nov_keyword + df_30_nov_news
            },
            'ca-related': {
                'ca': [df_30_nov_ca, "{:.4f}".format(df_30_nov_ca / float(df_30_nov_ca + df_30_nov_non_ca + df_30_nov_na) * 100)],
                'non-ca': [df_30_nov_non_ca, "{:.4f}".format(df_30_nov_non_ca / float(df_30_nov_ca + df_30_nov_non_ca + df_30_nov_na) * 100)],
                'na': [df_30_nov_na, "{:.4f}".format(df_30_nov_na / float(df_30_nov_ca + df_30_nov_non_ca + df_30_nov_na) * 100)],
                'sum': df_30_nov_ca + df_30_nov_non_ca + df_30_nov_na
            },
            'sentiment': {
                'pos': [df_30_nov_pos, "{:.4f}".format(df_30_nov_pos / float(df_30_nov_pos + df_30_nov_neg + df_30_nov_neut) * 100)],
                'neg': [df_30_nov_neg, "{:.4f}".format(df_30_nov_neg / float(df_30_nov_pos + df_30_nov_neg + df_30_nov_neut) * 100)],
                'neut': [df_30_nov_neut, "{:.4f}".format(df_30_nov_neut / float(df_30_nov_pos + df_30_nov_neg + df_30_nov_neut) * 100)],
                'sum': df_30_nov_pos + df_30_nov_neg + df_30_nov_neut
            },
            'labels': {
                'covid-controversy': [df_30_nov_controversy, "{:.4f}".format(df_30_nov_controversy / float(
                    df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency) * 100)],
                'covid-new-variant': [df_30_nov_new_variant, "{:.4f}".format(df_30_nov_new_variant / float(
                    df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency) * 100)],
                'pandemic-legal': [df_30_nov_legal, "{:.4f}".format(df_30_nov_legal / float(
                    df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency) * 100)],
                'pandemic-logistics': [df_30_nov_logistics, "{:.4f}".format(df_30_nov_logistics / float(
                    df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency) * 100)],
                'vax-efficiency': [df_30_nov_efficiency, "{:.4f}".format(df_30_nov_efficiency / float(
                    df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency) * 100)],
                'sum': df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency
            }
        },
        '01_dec': {
            'filter-type': {
                'gvnmt': [df_01_dec_gvnmt, "{:.4f}".format(df_01_dec_gvnmt / float(df_01_dec_gvnmt + df_01_dec_keyword + df_01_dec_news) * 100)],
                'keyword': [df_01_dec_keyword,
                            "{:.4f}".format(df_01_dec_keyword / float(df_01_dec_gvnmt + df_01_dec_keyword + df_01_dec_news) * 100)],
                'news': [df_01_dec_news, "{:.4f}".format(df_01_dec_news / float(df_01_dec_gvnmt + df_01_dec_keyword + df_01_dec_news) * 100)],
                'sum': df_01_dec_gvnmt + df_01_dec_keyword + df_01_dec_news
            },
            'ca-related': {
                'ca': [df_01_dec_ca, "{:.4f}".format(df_01_dec_ca / float(df_01_dec_ca + df_01_dec_non_ca + df_01_dec_na) * 100)],
                'non-ca': [df_01_dec_non_ca, "{:.4f}".format(df_01_dec_non_ca / float(df_01_dec_ca + df_01_dec_non_ca + df_01_dec_na) * 100)],
                'na': [df_01_dec_na, "{:.4f}".format(df_01_dec_na / float(df_01_dec_ca + df_01_dec_non_ca + df_01_dec_na) * 100)],
                'sum': df_01_dec_ca + df_01_dec_non_ca + df_01_dec_na
            },
            'sentiment': {
                'pos': [df_01_dec_pos, "{:.4f}".format(df_01_dec_pos / float(df_01_dec_pos + df_01_dec_neg + df_01_dec_neut) * 100)],
                'neg': [df_01_dec_neg, "{:.4f}".format(df_01_dec_neg / float(df_01_dec_pos + df_01_dec_neg + df_01_dec_neut) * 100)],
                'neut': [df_01_dec_neut, "{:.4f}".format(df_01_dec_neut / float(df_01_dec_pos + df_01_dec_neg + df_01_dec_neut) * 100)],
                'sum': df_01_dec_pos + df_01_dec_neg + df_01_dec_neut
            },
            'labels': {
                'covid-controversy': [df_01_dec_controversy, "{:.4f}".format(df_01_dec_controversy / float(
                    df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency) * 100)],
                'covid-new-variant': [df_01_dec_new_variant, "{:.4f}".format(df_01_dec_new_variant / float(
                    df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency) * 100)],
                'pandemic-legal': [df_01_dec_legal, "{:.4f}".format(df_01_dec_legal / float(
                    df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency) * 100)],
                'pandemic-logistics': [df_01_dec_logistics, "{:.4f}".format(df_01_dec_logistics / float(
                    df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency) * 100)],
                'vax-efficiency': [df_01_dec_efficiency, "{:.4f}".format(df_01_dec_efficiency / float(
                    df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency) * 100)],
                'sum': df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency
            }
        }
    }
    write_to_json(dict_stats_per_day, 'data/results/stats_per_day.json', write_param='w')


def generate_stats_per_filter_type():
    df_gvnmt_pos = df.loc[((df['filter_type'] == 'gvnmt') & (df['sentiment'] == 'pos'))].copy().shape[0]
    df_gvnmt_neg = df.loc[((df['filter_type'] == 'gvnmt') & (df['sentiment'] == 'neg'))].copy().shape[0]
    df_gvnmt_neut = df.loc[((df['filter_type'] == 'gvnmt') & (df['sentiment'] == 'neut'))].copy().shape[0]

    df_keyword_pos = df.loc[((df['filter_type'] == 'keyword') & (df['sentiment'] == 'pos'))].copy().shape[0]
    df_keyword_neg = df.loc[((df['filter_type'] == 'keyword') & (df['sentiment'] == 'neg'))].copy().shape[0]
    df_keyword_neut = df.loc[((df['filter_type'] == 'keyword') & (df['sentiment'] == 'neut'))].copy().shape[0]

    df_news_pos = df.loc[((df['filter_type'] == 'news') & (df['sentiment'] == 'pos'))].copy().shape[0]
    df_news_neg = df.loc[((df['filter_type'] == 'news') & (df['sentiment'] == 'neg'))].copy().shape[0]
    df_news_neut = df.loc[((df['filter_type'] == 'news') & (df['sentiment'] == 'neut'))].copy().shape[0]

    df_gvnmt_controversy = df.loc[((df['filter_type'] == 'gvnmt') & (df['labels'] == 'covid-controversy'))].copy().shape[0]
    df_gvnmt_new_variant = df.loc[((df['filter_type'] == 'gvnmt') & (df['labels'] == 'covid-new-variant'))].copy().shape[0]
    df_gvnmt_legal = df.loc[((df['filter_type'] == 'gvnmt') & (df['labels'] == 'pandemic-legal'))].copy().shape[0]
    df_gvnmt_logistics = df.loc[((df['filter_type'] == 'gvnmt') & (df['labels'] == 'pandemic-logistics'))].copy().shape[0]
    df_gvnmt_efficiency = df.loc[((df['filter_type'] == 'gvnmt') & (df['labels'] == 'vax-efficiency'))].copy().shape[0]

    df_keyword_controversy = df.loc[((df['filter_type'] == 'keyword') & (df['labels'] == 'covid-controversy'))].copy().shape[0]
    df_keyword_new_variant = df.loc[((df['filter_type'] == 'keyword') & (df['labels'] == 'covid-new-variant'))].copy().shape[0]
    df_keyword_legal = df.loc[((df['filter_type'] == 'keyword') & (df['labels'] == 'pandemic-legal'))].copy().shape[0]
    df_keyword_logistics = df.loc[((df['filter_type'] == 'keyword') & (df['labels'] == 'pandemic-logistics'))].copy().shape[0]
    df_keyword_efficiency = df.loc[((df['filter_type'] == 'keyword') & (df['labels'] == 'vax-efficiency'))].copy().shape[0]

    df_news_controversy = df.loc[((df['filter_type'] == 'news') & (df['labels'] == 'covid-controversy'))].copy().shape[0]
    df_news_new_variant = df.loc[((df['filter_type'] == 'news') & (df['labels'] == 'covid-new-variant'))].copy().shape[0]
    df_news_legal = df.loc[((df['filter_type'] == 'news') & (df['labels'] == 'pandemic-legal'))].copy().shape[0]
    df_news_logistics = df.loc[((df['filter_type'] == 'news') & (df['labels'] == 'pandemic-logistics'))].copy().shape[0]
    df_news_efficiency = df.loc[((df['filter_type'] == 'news') & (df['labels'] == 'vax-efficiency'))].copy().shape[0]

    df_gvnmt_ca = df.loc[((df['filter_type'] == 'gvnmt') & (df['ca_related'] == 'ca'))].copy().shape[0]
    df_gvnmt_non_ca = df.loc[((df['filter_type'] == 'gvnmt') & (df['ca_related'] == 'non-ca'))].copy().shape[0]
    df_gvnmt_na = df.loc[((df['filter_type'] == 'gvnmt') & (df['ca_related'] == 'na'))].copy().shape[0]

    df_keyword_ca = df.loc[((df['filter_type'] == 'keyword') & (df['ca_related'] == 'ca'))].copy().shape[0]
    df_keyword_non_ca = df.loc[((df['filter_type'] == 'keyword') & (df['ca_related'] == 'non-ca'))].copy().shape[0]
    df_keyword_na = df.loc[((df['filter_type'] == 'keyword') & (df['ca_related'] == 'na'))].copy().shape[0]

    df_news_ca = df.loc[((df['filter_type'] == 'news') & (df['ca_related'] == 'ca'))].copy().shape[0]
    df_news_non_ca = df.loc[((df['filter_type'] == 'news') & (df['ca_related'] == 'non-ca'))].copy().shape[0]
    df_news_na = df.loc[((df['filter_type'] == 'news') & (df['ca_related'] == 'na'))].copy().shape[0]

    dict_stats_per_filter_type = {
        'gvnmt': {
            'sentiment': {
                'pos': [df_gvnmt_pos,
                        "{:.4f}".format(df_gvnmt_pos / float(df_gvnmt_pos + df_gvnmt_neg + df_gvnmt_neut) * 100)],
                'neg': [df_gvnmt_neg,
                        "{:.4f}".format(df_gvnmt_neg / float(df_gvnmt_pos + df_gvnmt_neg + df_gvnmt_neut) * 100)],
                'neut': [df_gvnmt_neut,
                       "{:.4f}".format(df_gvnmt_neut / float(df_gvnmt_pos + df_gvnmt_neg + df_gvnmt_neut) * 100)],
                'sum': df_gvnmt_pos + df_gvnmt_neg + df_gvnmt_neut
            },
            'label': {
                'covid-controversy': [df_gvnmt_controversy, "{:.4f}".format(df_gvnmt_controversy / float(
                    df_gvnmt_controversy + df_gvnmt_new_variant + df_gvnmt_legal + df_gvnmt_logistics + df_gvnmt_efficiency) * 100)],
                'covid-new-variant': [df_gvnmt_new_variant, "{:.4f}".format(df_gvnmt_new_variant / float(
                    df_gvnmt_controversy + df_gvnmt_new_variant + df_gvnmt_legal + df_gvnmt_logistics + df_gvnmt_efficiency) * 100)],
                'pandemic-legal': [df_gvnmt_legal, "{:.4f}".format(df_gvnmt_legal / float(
                    df_gvnmt_controversy + df_gvnmt_new_variant + df_gvnmt_legal + df_gvnmt_logistics + df_gvnmt_efficiency) * 100)],
                'pandemic-logistics': [df_gvnmt_logistics, "{:.4f}".format(df_gvnmt_logistics / float(
                    df_gvnmt_controversy + df_gvnmt_new_variant + df_gvnmt_legal + df_gvnmt_logistics + df_gvnmt_efficiency) * 100)],
                'vax-efficiency': [df_gvnmt_efficiency, "{:.4f}".format(df_gvnmt_efficiency / float(
                    df_gvnmt_controversy + df_gvnmt_new_variant + df_gvnmt_legal + df_gvnmt_logistics + df_gvnmt_efficiency) * 100)],
                'sum': df_gvnmt_controversy + df_gvnmt_new_variant + df_gvnmt_legal + df_gvnmt_logistics + df_gvnmt_efficiency
            },
            'ca-related': {
                'ca': [df_gvnmt_ca,
                       "{:.4f}".format(df_gvnmt_ca / float(df_gvnmt_ca + df_gvnmt_non_ca + df_gvnmt_na) * 100)],
                'non-ca': [df_gvnmt_non_ca,
                           "{:.4f}".format(df_gvnmt_non_ca / float(df_gvnmt_ca + df_gvnmt_non_ca + df_gvnmt_na) * 100)],
                'na': [df_gvnmt_na,
                       "{:.4f}".format(df_gvnmt_na / float(df_gvnmt_ca + df_gvnmt_non_ca + df_gvnmt_na) * 100)],
                'sum': df_gvnmt_ca + df_gvnmt_non_ca + df_gvnmt_na
            }
        },
        'keyword': {
            'sentiment': {
                'pos': [df_keyword_pos,
                        "{:.4f}".format(
                            df_keyword_pos / float(df_keyword_pos + df_keyword_neg + df_keyword_neut) * 100)],
                'neg': [df_keyword_neg,
                        "{:.4f}".format(
                            df_keyword_neg / float(df_keyword_pos + df_keyword_neg + df_keyword_neut) * 100)],
                'neut': [df_keyword_neut,
                       "{:.4f}".format(
                           df_keyword_neut / float(df_keyword_pos + df_keyword_neg + df_keyword_neut) * 100)],
                'sum': df_keyword_pos + df_keyword_neg + df_keyword_neut
            },
            'label': {
                'covid-controversy': [df_keyword_controversy, "{:.4f}".format(df_keyword_controversy / float(
                    df_keyword_controversy + df_keyword_new_variant + df_keyword_legal + df_keyword_logistics + df_keyword_efficiency) * 100)],
                'covid-new-variant': [df_keyword_new_variant, "{:.4f}".format(df_keyword_new_variant / float(
                    df_keyword_controversy + df_keyword_new_variant + df_keyword_legal + df_keyword_logistics + df_keyword_efficiency) * 100)],
                'pandemic-legal': [df_keyword_legal, "{:.4f}".format(df_keyword_legal / float(
                    df_keyword_controversy + df_keyword_new_variant + df_keyword_legal + df_keyword_logistics + df_keyword_efficiency) * 100)],
                'pandemic-logistics': [df_keyword_logistics, "{:.4f}".format(df_keyword_logistics / float(
                    df_keyword_controversy + df_keyword_new_variant + df_keyword_legal + df_keyword_logistics + df_keyword_efficiency) * 100)],
                'vax-efficiency': [df_keyword_efficiency, "{:.4f}".format(df_keyword_efficiency / float(
                    df_keyword_controversy + df_keyword_new_variant + df_keyword_legal + df_keyword_logistics + df_keyword_efficiency) * 100)],
                'sum': df_keyword_controversy + df_keyword_new_variant + df_keyword_legal + df_keyword_logistics + df_keyword_efficiency
            },
            'ca-related': {
                'ca': [df_keyword_ca,
                       "{:.4f}".format(df_keyword_ca / float(df_keyword_ca + df_keyword_non_ca + df_keyword_na) * 100)],
                'non-ca': [df_keyword_non_ca,
                           "{:.4f}".format(
                               df_keyword_non_ca / float(df_keyword_ca + df_keyword_non_ca + df_keyword_na) * 100)],
                'na': [df_keyword_na,
                       "{:.4f}".format(df_keyword_na / float(df_keyword_ca + df_keyword_non_ca + df_keyword_na) * 100)],
                'sum': df_keyword_ca + df_keyword_non_ca + df_keyword_na
            }
        },
        'news': {
            'sentiment': {
                'pos': [df_news_pos,
                        "{:.4f}".format(
                            df_news_pos / float(df_news_pos + df_news_neg + df_news_neut) * 100)],
                'neg': [df_news_neg,
                        "{:.4f}".format(
                            df_news_neg / float(df_news_pos + df_news_neg + df_news_neut) * 100)],
                'neut': [df_news_neut,
                       "{:.4f}".format(
                           df_news_neut / float(df_news_pos + df_news_neg + df_news_neut) * 100)],
                'sum': df_news_pos + df_news_neg + df_news_neut
            },
            'label': {
                'covid-controversy': [df_news_controversy, "{:.4f}".format(df_news_controversy / float(
                    df_news_controversy + df_news_new_variant + df_news_legal + df_news_logistics + df_news_efficiency) * 100)],
                'covid-new-variant': [df_news_new_variant, "{:.4f}".format(df_news_new_variant / float(
                    df_news_controversy + df_news_new_variant + df_news_legal + df_news_logistics + df_news_efficiency) * 100)],
                'pandemic-legal': [df_news_legal, "{:.4f}".format(df_news_legal / float(
                    df_news_controversy + df_news_new_variant + df_news_legal + df_news_logistics + df_news_efficiency) * 100)],
                'pandemic-logistics': [df_news_logistics, "{:.4f}".format(df_news_logistics / float(
                    df_news_controversy + df_news_new_variant + df_news_legal + df_news_logistics + df_news_efficiency) * 100)],
                'vax-efficiency': [df_news_efficiency, "{:.4f}".format(df_news_efficiency / float(
                    df_news_controversy + df_news_new_variant + df_news_legal + df_news_logistics + df_news_efficiency) * 100)],
                'sum': df_news_controversy + df_news_new_variant + df_news_legal + df_news_logistics + df_news_efficiency
            },
            'ca-related': {
                'ca': [df_news_ca,
                       "{:.4f}".format(df_news_ca / float(df_news_ca + df_news_non_ca + df_news_na) * 100)],
                'non-ca': [df_news_non_ca,
                           "{:.4f}".format(
                               df_news_non_ca / float(df_news_ca + df_news_non_ca + df_news_na) * 100)],
                'na': [df_news_na,
                       "{:.4f}".format(df_news_na / float(df_news_ca + df_news_non_ca + df_news_na) * 100)],
                'sum': df_news_ca + df_news_non_ca + df_news_na
            }
        }
    }
    write_to_json(dict_stats_per_filter_type, 'data/results/stats_per_filter_type.json', write_param='w')


def generate_stats_per_covid_label():
    df_controversy_pos = df.loc[(df['labels'] == 'covid-controversy') & (df['sentiment'] == 'pos')].copy().shape[0]
    df_controversy_neg = df.loc[(df['labels'] == 'covid-controversy') & (df['sentiment'] == 'neg')].copy().shape[0]
    df_controversy_neut = df.loc[(df['labels'] == 'covid-controversy') & (df['sentiment'] == 'neut')].copy().shape[0]
    df_controversy_ca = df.loc[(df['labels'] == 'covid-controversy') & (df['ca_related'] == 'ca')].copy().shape[0]
    df_controversy_non_ca = df.loc[(df['labels'] == 'covid-controversy') & (df['ca_related'] == 'non-ca')].copy().shape[0]
    df_controversy_na = df.loc[(df['labels'] == 'covid-controversy') & (df['ca_related'] == 'na')].copy().shape[0]
    df_new_variant_pos = df.loc[(df['labels'] == 'covid-new-variant') & (df['sentiment'] == 'pos')].copy().shape[0]
    df_new_variant_neg = df.loc[(df['labels'] == 'covid-new-variant') & (df['sentiment'] == 'neg')].copy().shape[0]
    df_new_variant_neut = df.loc[(df['labels'] == 'covid-new-variant') & (df['sentiment'] == 'neut')].copy().shape[0]
    df_new_variant_ca = df.loc[(df['labels'] == 'covid-new-variant') & (df['ca_related'] == 'ca')].copy().shape[0]
    df_new_variant_non_ca = df.loc[(df['labels'] == 'covid-new-variant') & (df['ca_related'] == 'non-ca')].copy().shape[0]
    df_new_variant_na = df.loc[(df['labels'] == 'covid-new-variant') & (df['ca_related'] == 'na')].copy().shape[0]
    df_legal_pos = df.loc[(df['labels'] == 'pandemic-legal') & (df['sentiment'] == 'pos')].copy().shape[0]
    df_legal_neg = df.loc[(df['labels'] == 'pandemic-legal') & (df['sentiment'] == 'neg')].copy().shape[0]
    df_legal_neut = df.loc[(df['labels'] == 'pandemic-legal') & (df['sentiment'] == 'neut')].copy().shape[0]
    df_legal_ca = df.loc[(df['labels'] == 'pandemic-legal') & (df['ca_related'] == 'ca')].copy().shape[0]
    df_legal_non_ca = df.loc[(df['labels'] == 'pandemic-legal') & (df['ca_related'] == 'non-ca')].copy().shape[0]
    df_legal_na = df.loc[(df['labels'] == 'pandemic-legal') & (df['ca_related'] == 'na')].copy().shape[0]
    df_logistics_pos = df.loc[(df['labels'] == 'pandemic-logistics') & (df['sentiment'] == 'pos')].copy().shape[0]
    df_logistics_neg = df.loc[(df['labels'] == 'pandemic-logistics') & (df['sentiment'] == 'neg')].copy().shape[0]
    df_logistics_neut = df.loc[(df['labels'] == 'pandemic-logistics') & (df['sentiment'] == 'neut')].copy().shape[0]
    df_logistics_ca = df.loc[(df['labels'] == 'pandemic-logistics') & (df['ca_related'] == 'ca')].copy().shape[0]
    df_logistics_non_ca = df.loc[(df['labels'] == 'pandemic-logistics') & (df['ca_related'] == 'non-ca')].copy().shape[0]
    df_logistics_na = df.loc[(df['labels'] == 'pandemic-logistics') & (df['ca_related'] == 'na')].copy().shape[0]
    df_efficiency_pos = df.loc[(df['labels'] == 'vax-efficiency') & (df['sentiment'] == 'pos')].copy().shape[0]
    df_efficiency_neg = df.loc[(df['labels'] == 'vax-efficiency') & (df['sentiment'] == 'neg')].copy().shape[0]
    df_efficiency_neut = df.loc[(df['labels'] == 'vax-efficiency') & (df['sentiment'] == 'neut')].copy().shape[0]
    df_efficiency_ca = df.loc[(df['labels'] == 'vax-efficiency') & (df['ca_related'] == 'ca')].copy().shape[0]
    df_efficiency_non_ca = df.loc[(df['labels'] == 'vax-efficiency') & (df['ca_related'] == 'non-ca')].copy().shape[0]
    df_efficiency_na = df.loc[(df['labels'] == 'vax-efficiency') & (df['ca_related'] == 'na')].copy().shape[0]
    dict_stats_per_covid_label = {
        'covid-controversy': {
            'sentiment': {
                'pos': [df_controversy_pos,
                        "{:.4f}".format(df_controversy_pos / float(df_controversy_pos + df_controversy_neg + df_controversy_neut) * 100)],
                'neg': [df_controversy_neg,
                        "{:.4f}".format(df_controversy_neg / float(df_controversy_pos + df_controversy_neg + df_controversy_neut) * 100)],
                'neut': [df_controversy_neut,
                         "{:.4f}".format(df_controversy_neut / float(df_controversy_pos + df_controversy_neg + df_controversy_neut) * 100)],
                'sum': df_controversy_pos + df_controversy_neg + df_controversy_neut
            },
            'ca-related': {
                'ca': [df_controversy_ca,
                       "{:.4f}".format(df_controversy_ca / float(df_controversy_ca + df_controversy_non_ca + df_controversy_na) * 100)],
                'non-ca': [df_controversy_non_ca,
                           "{:.4f}".format(df_controversy_non_ca / float(df_controversy_ca + df_controversy_non_ca + df_controversy_na) * 100)],
                'na': [df_controversy_na,
                       "{:.4f}".format(df_controversy_na / float(df_controversy_ca + df_controversy_non_ca + df_controversy_na) * 100)],
                'sum': df_controversy_ca + df_controversy_non_ca + df_controversy_na
            }
        },
        'covid-new-variant': {
            'sentiment': {
                'pos': [df_new_variant_pos,
                        "{:.4f}".format(df_new_variant_pos / float(df_new_variant_pos + df_new_variant_neg + df_new_variant_neut) * 100)],
                'neg': [df_new_variant_neg,
                        "{:.4f}".format(df_new_variant_neg / float(df_new_variant_pos + df_new_variant_neg + df_new_variant_neut) * 100)],
                'neut': [df_new_variant_neut,
                         "{:.4f}".format(df_new_variant_neut / float(df_new_variant_pos + df_new_variant_neg + df_new_variant_neut) * 100)],
                'sum': df_new_variant_pos + df_new_variant_neg + df_new_variant_neut
            },
            'ca-related': {
                'ca': [df_new_variant_ca,
                       "{:.4f}".format(df_new_variant_ca / float(df_new_variant_ca + df_new_variant_non_ca + df_new_variant_na) * 100)],
                'non-ca': [df_new_variant_non_ca,
                           "{:.4f}".format(df_new_variant_non_ca / float(df_new_variant_ca + df_new_variant_non_ca + df_new_variant_na) * 100)],
                'na': [df_new_variant_na,
                       "{:.4f}".format(df_new_variant_na / float(df_new_variant_ca + df_new_variant_non_ca + df_new_variant_na) * 100)],
                'sum': df_new_variant_ca + df_new_variant_non_ca + df_new_variant_na
            }
        },
        'pandemic-legal': {
            'sentiment': {
                'pos': [df_legal_pos,
                        "{:.4f}".format(df_legal_pos / float(df_legal_pos + df_legal_neg + df_legal_neut) * 100)],
                'neg': [df_legal_neg,
                        "{:.4f}".format(df_legal_neg / float(df_legal_pos + df_legal_neg + df_legal_neut) * 100)],
                'neut': [df_legal_neut,
                         "{:.4f}".format(df_legal_neut / float(df_legal_pos + df_legal_neg + df_legal_neut) * 100)],
                'sum': df_legal_pos + df_legal_neg + df_legal_neut
            },
            'ca-related': {
                'ca': [df_legal_ca,
                       "{:.4f}".format(df_legal_ca / float(df_legal_ca + df_legal_non_ca + df_legal_na) * 100)],
                'non-ca': [df_legal_non_ca,
                           "{:.4f}".format(df_legal_non_ca / float(df_legal_ca + df_legal_non_ca + df_legal_na) * 100)],
                'neut': [df_legal_na,
                         "{:.4f}".format(df_legal_na / float(df_legal_ca + df_legal_non_ca + df_legal_na) * 100)],
                'sum': df_legal_ca + df_legal_non_ca + df_legal_na
            }
        },
        'pandemic-logistics': {
            'sentiment': {
                'pos': [df_logistics_pos,
                        "{:.4f}".format(df_logistics_pos / float(df_logistics_pos + df_logistics_neg + df_logistics_neut) * 100)],
                'neg': [df_logistics_neg,
                        "{:.4f}".format(df_logistics_neg / float(df_logistics_pos + df_logistics_neg + df_logistics_neut) * 100)],
                'neut': [df_logistics_neut,
                         "{:.4f}".format(df_logistics_neut / float(df_logistics_pos + df_logistics_neg + df_logistics_neut) * 100)],
                'sum': df_logistics_pos + df_logistics_neg + df_logistics_neut
            },
            'ca-related': {
                'ca': [df_logistics_ca,
                       "{:.4f}".format(df_logistics_ca / float(df_logistics_ca + df_logistics_non_ca + df_logistics_na) * 100)],
                'non-ca': [df_logistics_non_ca,
                           "{:.4f}".format(df_logistics_non_ca / float(df_logistics_ca + df_logistics_non_ca + df_logistics_na) * 100)],
                'na': [df_logistics_na,
                       "{:.4f}".format(df_logistics_na / float(df_logistics_ca + df_logistics_non_ca + df_logistics_na) * 100)],
                'sum': df_logistics_ca + df_logistics_non_ca + df_logistics_na
            }
        },
        'vax-efficiency': {
            'sentiment': {
                'pos': [df_efficiency_pos,
                        "{:.4f}".format(df_efficiency_pos / float(df_efficiency_pos + df_efficiency_neg + df_efficiency_neut) * 100)],
                'neg': [df_efficiency_neg,
                        "{:.4f}".format(df_efficiency_neg / float(df_efficiency_pos + df_efficiency_neg + df_efficiency_neut) * 100)],
                'neut': [df_efficiency_neut,
                         "{:.4f}".format(df_efficiency_neut / float(df_efficiency_pos + df_efficiency_neg + df_efficiency_neut) * 100)],
                'sum': df_efficiency_pos + df_efficiency_neg + df_efficiency_neut
            },
            'ca-related': {
                'ca': [df_efficiency_ca,
                       "{:.4f}".format(df_efficiency_ca / float(df_efficiency_ca + df_efficiency_non_ca + df_efficiency_na) * 100)],
                'non-ca': [df_efficiency_non_ca,
                           "{:.4f}".format(df_efficiency_non_ca / float(df_efficiency_ca + df_efficiency_non_ca + df_efficiency_na) * 100)],
                'na': [df_efficiency_na,
                       "{:.4f}".format(df_efficiency_na / float(df_efficiency_ca + df_efficiency_non_ca + df_efficiency_na) * 100)],
                'sum': df_efficiency_ca + df_efficiency_non_ca + df_efficiency_na
            }
        }
    }
    write_to_json(dict_stats_per_covid_label, 'data/results/stats_per_covid_label.json', write_param='w')


if __name__ == '__main__':
    df = read_from_csv_collected_tweets(ALL_TWEETS_CSV)

    # generate_stats_per_label()
    # generate_stats_per_day()
    # generate_stats_per_filter_type()
    # generate_stats_per_covid_label()

    print()
