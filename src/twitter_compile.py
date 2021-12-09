from twitter_collect import read_from_csv_collected_tweets

paths = [
    'data/annotated_final/dec_01_twitter_dump_by_keywords_final.csv',
    'data/annotated_final/nov_30_twitter_dump_by_keywords_final.csv',
    'data/annotated_final/nov_29_twitter_dump_by_keywords_final.csv',
    'data/annotated_final/dec_01_twitter_dump_replies_gvmnt_only_final.csv',
    'data/annotated_final/nov_30_twitter_dump_replies_gvmnt_only_final.csv',
    'data/annotated_final/nov_29_twitter_dump_replies_gvmnt_only_final.csv',
    'data/annotated_final/dec_01_twitter_dump_replies_news_channels_only_final.csv'
    'data/annotated_final/nov_30_twitter_dump_replies_news_channels_only_final.csv'
    'data/annotated_final/nov_29_twitter_dump_replies_news_channels_only_final.csv'
]


if __name__ == '__main__':
    df = read_from_csv_collected_tweets(paths[0])
    print()