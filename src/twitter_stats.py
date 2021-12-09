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


if __name__ == '__main__':
    df = read_from_csv_collected_tweets(ALL_TWEETS_CSV)

    df_pos_only = df.loc[df['sentiment'] == 'pos'].copy()
    df_neg_only = df.loc[df['sentiment'] == 'neg'].copy()
    df_neut_only = df.loc[df['sentiment'] == 'neut'].copy()

    df_controversy_only = df.loc[df['labels'] == 'covid-controversy'].copy()
    df_new_variant_only = df.loc[df['labels'] == 'covid-new-variant'].copy()
    df_legal_only = df.loc[df['labels'] == 'pandemic-legal'].copy()
    df_logistics_only = df.loc[df['labels'] == 'pandemic-logistics'].copy()
    df_efficiency_only = df.loc[df['labels'] == 'vax-efficiency'].copy()

    df_ca_only = df.loc[df['ca_related'] == 'ca'].copy()
    df_non_ca_only = df.loc[df['ca_related'] == 'non-ca'].copy()
    df_na_only = df.loc[df['ca_related'] == 'na'].copy()

    df_01_dec_only = df.loc[df['day'] == '01_dec'].copy()
    df_30_nov_only = df.loc[df['day'] == '30_nov'].copy()
    df_29_nov_only = df.loc[df['day'] == '29_nov'].copy()

    df_gvnmt_only = df.loc[df['filter_type'] == 'gvnmt'].copy()
    df_keyword_only = df.loc[df['filter_type'] == 'keyword'].copy()
    df_news_only = df.loc[df['filter_type'] == 'news'].copy()

    dict_stats_per_label = {
        'sentiment': {
            'pos': df_pos_only.shape[0],
            'neg': df_neg_only.shape[0],
            'neut': df_neut_only.shape[0]
        },
        'labels': {
            'covid-controversy': df_controversy_only.shape[0],
            'covid-new-variant': df_new_variant_only.shape[0],
            'pandemic-legal': df_legal_only.shape[0],
            'covid-logistics': df_logistics_only.shape[0],
            'vax-efficiency': df_efficiency_only.shape[0],
        },
        'ca_related': {
            'ca': df_ca_only.shape[0],
            'non-ca': df_non_ca_only.shape[0],
            'na': df_na_only.shape[0],
        },
        'day': {
            '01-dec': df_01_dec_only.shape[0],
            '30-nov': df_30_nov_only.shape[0],
            '29-nov': df_29_nov_only.shape[0],
        },
        'filter-type': {
            'gvnmt': df_gvnmt_only.shape[0],
            'keyword': df_keyword_only.shape[0],
            'news': df_news_only.shape[0],
        }
    }

    write_to_json(dict_stats_per_label, 'data/results/stats_per_label.json')
    print()
