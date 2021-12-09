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
            'pos': [df_pos_only, "{:.4f}".format(df_pos_only / float(df_pos_only + df_neg_only + df_neut_only)*100)],
            'neg': [df_neg_only, "{:.4f}".format(df_neg_only / float(df_pos_only + df_neg_only + df_neut_only)*100)],
            'neut': [df_neut_only, "{:.4f}".format(df_neut_only / float(df_pos_only + df_neg_only + df_neut_only)*100)],
            'sum': df_pos_only + df_neg_only + df_neut_only
        },
        'labels': {
            'covid-controversy': [df_controversy_only, "{:.4f}".format(df_controversy_only / float(df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only)*100)],
            'covid-new-variant': [df_new_variant_only, "{:.4f}".format(df_new_variant_only / float(df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only)*100)],
            'pandemic-legal': [df_legal_only, "{:.4f}".format(df_legal_only / float(df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only)*100)],
            'covid-logistics': [df_logistics_only, "{:.4f}".format(df_logistics_only / float(df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only)*100)],
            'vax-efficiency': [df_efficiency_only, "{:.4f}".format(df_efficiency_only / float(df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only)*100)],
            'sum': df_controversy_only + df_new_variant_only + df_legal_only + df_logistics_only + df_efficiency_only
        },
        'ca-related': {
            'ca': [df_ca_only, "{:.4f}".format(df_ca_only / float(df_ca_only + df_non_ca_only + df_na_only)*100)],
            'non-ca': [df_non_ca_only, "{:.4f}".format(df_non_ca_only / float(df_ca_only + df_non_ca_only + df_na_only)*100)],
            'na': [df_na_only, "{:.4f}".format(df_na_only / float(df_ca_only + df_non_ca_only + df_na_only)*100)],
            'sum': df_ca_only + df_non_ca_only + df_na_only
        },
        'day': {
            '01-dec': [df_01_dec_only, "{:.4f}".format(df_01_dec_only / float(df_01_dec_only + df_30_nov_only + df_29_nov_only)*100)],
            '30-nov': [df_30_nov_only, "{:.4f}".format(df_30_nov_only / float(df_01_dec_only + df_30_nov_only + df_29_nov_only)*100)],
            '29-nov': [df_29_nov_only, "{:.4f}".format(df_29_nov_only / float(df_01_dec_only + df_30_nov_only + df_29_nov_only)*100)],
            'sum': df_01_dec_only + df_30_nov_only + df_29_nov_only
        },
        'filter-type': {
            'gvnmt': [df_gvnmt_only, "{:.4f}".format(df_gvnmt_only / float(df_gvnmt_only + df_keyword_only + df_news_only)*100)],
            'keyword': [df_keyword_only, "{:.4f}".format(df_keyword_only / float(df_gvnmt_only + df_keyword_only + df_news_only)*100)],
            'news': [df_news_only, "{:.4f}".format(df_news_only / float(df_gvnmt_only + df_keyword_only + df_news_only)*100)],
            'sum': df_gvnmt_only + df_keyword_only + df_news_only
        }
    }
    write_to_json(dict_stats_per_label, 'data/results/stats_per_label.json', write_param='w')


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
                'gvnmt': [df_29_nov_gvnmt, "{:.4f}".format(df_29_nov_news / float(df_29_nov_gvnmt + df_29_nov_keyword + df_29_nov_news)*100)],
                'keyword': [df_29_nov_keyword, "{:.4f}".format(df_29_nov_keyword / float(df_29_nov_gvnmt + df_29_nov_keyword + df_29_nov_news)*100)],
                'news': [df_29_nov_news, "{:.4f}".format(df_29_nov_news / float(df_29_nov_gvnmt + df_29_nov_keyword + df_29_nov_news)*100)],
                'sum': df_29_nov_gvnmt + df_29_nov_keyword + df_29_nov_news
            },
            'ca-related': {
                'ca': [df_29_nov_ca, "{:.4f}".format(df_29_nov_ca / float(df_29_nov_ca + df_29_nov_non_ca + df_29_nov_na)*100)],
                'non-ca': [df_29_nov_non_ca, "{:.4f}".format(df_29_nov_non_ca / float(df_29_nov_ca + df_29_nov_non_ca + df_29_nov_na)*100)],
                'na': [df_29_nov_na,"{:.4f}".format(df_29_nov_na / float(df_29_nov_ca + df_29_nov_non_ca + df_29_nov_na)*100)],
                'sum': df_29_nov_ca + df_29_nov_non_ca + df_29_nov_na
            },
            'sentiment': {
                'pos': [df_29_nov_pos,"{:.4f}".format(df_29_nov_pos / float(df_29_nov_pos + df_29_nov_neg + df_29_nov_neut)*100)],
                'neg': [df_29_nov_neg,"{:.4f}".format(df_29_nov_neg / float(df_29_nov_pos + df_29_nov_neg + df_29_nov_neut)*100)],
                'neut': [df_29_nov_neut, "{:.4f}".format(df_29_nov_neut / float(df_29_nov_pos + df_29_nov_neg + df_29_nov_neut)*100)],
                'sum': df_29_nov_pos + df_29_nov_neg + df_29_nov_neut
            },
            'labels': {
                'covid-controversy': [df_29_nov_controversy, "{:.4f}".format(df_29_nov_controversy / float(df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency)*100)],
                'covid-new-variant': [df_29_nov_new_variant, "{:.4f}".format(df_29_nov_new_variant / float(df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency)*100)],
                'pandemic-legal': [df_29_nov_legal, "{:.4f}".format(df_29_nov_legal / float(df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency)*100)],
                'pandemic-logistics': [df_29_nov_logistics, "{:.4f}".format(df_29_nov_logistics / float(df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency)*100)],
                'vax-efficiency': [df_29_nov_efficiency, "{:.4f}".format(df_29_nov_efficiency / float(df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency)*100)],
                'sum': df_29_nov_controversy + df_29_nov_new_variant + df_29_nov_legal + df_29_nov_logistics + df_29_nov_efficiency
            }
        },
        '30_nov': {
            'filter-type': {
                'gvnmt': [df_30_nov_gvnmt, "{:.4f}".format(df_30_nov_gvnmt / float(df_30_nov_gvnmt + df_30_nov_keyword + df_30_nov_news)*100)],
                'keyword': [df_30_nov_keyword, "{:.4f}".format(df_30_nov_keyword / float(df_30_nov_gvnmt + df_30_nov_keyword + df_30_nov_news)*100)],
                'news': [df_30_nov_news, "{:.4f}".format(df_30_nov_news / float(df_30_nov_gvnmt + df_30_nov_keyword + df_30_nov_news)*100)],
                'sum': df_30_nov_gvnmt + df_30_nov_keyword + df_30_nov_news
            },
            'ca-related': {
                'ca': [df_30_nov_ca, "{:.4f}".format(df_30_nov_ca / float(df_30_nov_ca + df_30_nov_non_ca + df_30_nov_na)*100)],
                'non-ca': [df_30_nov_non_ca, "{:.4f}".format(df_30_nov_non_ca / float(df_30_nov_ca + df_30_nov_non_ca + df_30_nov_na)*100)],
                'na': [df_30_nov_na, "{:.4f}".format(df_30_nov_na / float(df_30_nov_ca + df_30_nov_non_ca + df_30_nov_na)*100)],
                'sum': df_30_nov_ca + df_30_nov_non_ca + df_30_nov_na
            },
            'sentiment': {
                'pos': [df_30_nov_pos, "{:.4f}".format(df_30_nov_pos / float(df_30_nov_pos + df_30_nov_neg + df_30_nov_neut)*100)],
                'neg': [df_30_nov_neg, "{:.4f}".format(df_30_nov_neg / float(df_30_nov_pos + df_30_nov_neg + df_30_nov_neut)*100)],
                'neut': [df_30_nov_neut, "{:.4f}".format(df_30_nov_neut / float(df_30_nov_pos + df_30_nov_neg + df_30_nov_neut)*100)],
                'sum': df_30_nov_pos + df_30_nov_neg + df_30_nov_neut
            },
            'labels': {
                'covid-controversy': [df_30_nov_controversy, "{:.4f}".format(df_30_nov_controversy / float(df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency)*100)],
                'covid-new-variant': [df_30_nov_new_variant, "{:.4f}".format(df_30_nov_new_variant / float(df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency)*100)],
                'pandemic-legal': [df_30_nov_legal, "{:.4f}".format(df_30_nov_legal / float(df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency)*100)],
                'pandemic-logistics': [df_30_nov_logistics, "{:.4f}".format(df_30_nov_logistics / float(df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency)*100)],
                'vax-efficiency': [df_30_nov_efficiency, "{:.4f}".format(df_30_nov_efficiency / float(df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency)*100)],
                'sum': df_30_nov_controversy + df_30_nov_new_variant + df_30_nov_legal + df_30_nov_logistics + df_30_nov_efficiency
            }
        },
        '01_dec': {
            'filter-type': {
                'gvnmt': [df_01_dec_gvnmt, "{:.4f}".format(df_01_dec_gvnmt / float(df_01_dec_gvnmt + df_01_dec_keyword + df_01_dec_news)*100)],
                'keyword': [df_01_dec_keyword, "{:.4f}".format(df_01_dec_keyword / float(df_01_dec_gvnmt + df_01_dec_keyword + df_01_dec_news)*100)],
                'news': [df_01_dec_news, "{:.4f}".format(df_01_dec_news / float(df_01_dec_gvnmt + df_01_dec_keyword + df_01_dec_news)*100)],
                'sum': df_01_dec_gvnmt + df_01_dec_keyword + df_01_dec_news
            },
            'ca-related': {
                'ca': [df_01_dec_ca, "{:.4f}".format(df_01_dec_ca / float(df_01_dec_ca + df_01_dec_non_ca + df_01_dec_na)*100)],
                'non-ca': [df_01_dec_non_ca, "{:.4f}".format(df_01_dec_non_ca / float(df_01_dec_ca + df_01_dec_non_ca + df_01_dec_na)*100)],
                'na': [df_01_dec_na, "{:.4f}".format(df_01_dec_na / float(df_01_dec_ca + df_01_dec_non_ca + df_01_dec_na)*100)],
                'sum': df_01_dec_ca + df_01_dec_non_ca + df_01_dec_na
            },
            'sentiment': {
                'pos': [df_01_dec_pos, "{:.4f}".format(df_01_dec_pos / float(df_01_dec_pos + df_01_dec_neg + df_01_dec_neut)*100)],
                'neg': [df_01_dec_neg, "{:.4f}".format(df_01_dec_neg / float(df_01_dec_pos + df_01_dec_neg + df_01_dec_neut)*100)],
                'neut': [df_01_dec_neut, "{:.4f}".format(df_01_dec_neut / float(df_01_dec_pos + df_01_dec_neg + df_01_dec_neut)*100)],
                'sum': df_01_dec_pos + df_01_dec_neg + df_01_dec_neut
            },
            'labels': {
                'covid-controversy': [df_01_dec_controversy, "{:.4f}".format(df_01_dec_controversy / float(df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency)*100)],
                'covid-new-variant': [df_01_dec_new_variant, "{:.4f}".format(df_01_dec_new_variant / float(df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency)*100)],
                'pandemic-legal': [df_01_dec_legal, "{:.4f}".format(df_01_dec_legal / float(df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency)*100)],
                'pandemic-logistics': [df_01_dec_logistics, "{:.4f}".format(df_01_dec_logistics / float(df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency)*100)],
                'vax-efficiency': [df_01_dec_efficiency, "{:.4f}".format(df_01_dec_efficiency / float(df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency)*100)],
                'sum': df_01_dec_controversy + df_01_dec_new_variant + df_01_dec_legal + df_01_dec_logistics + df_01_dec_efficiency
            }
        }
    }
    write_to_json(dict_stats_per_day, 'data/results/stats_per_day.json', write_param='w')


if __name__ == '__main__':
    df = read_from_csv_collected_tweets(ALL_TWEETS_CSV)
    generate_stats_per_label()
    generate_stats_per_day()

    print()
