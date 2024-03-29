import os.path
from pathlib import Path
from twitter_collect import get_file_paths, read_from_csv_collected_tweets, append_to_csv

SAMPLE_SIZE = 50

parentdir = Path(__file__).parents[1]

def main(USE_FILTER, FILE_PREFIX):
    global OUT_FILE_JSON, OUT_FILE_CSV, OUT_FILE_FILTERED_CSV, OUT_FILE_FILTERED_JSON, SEARCH_QUERY
    OUT_FILE_JSON, OUT_FILE_CSV, OUT_FILE_FILTERED_CSV, OUT_FILE_FILTERED_JSON, SEARCH_QUERY = get_file_paths(
        USE_FILTER, FILE_PREFIX)

    df = read_from_csv_collected_tweets(OUT_FILE_FILTERED_CSV)
    df_sample = None
    if df.shape[0] > SAMPLE_SIZE:
        df_sample = df.sample(SAMPLE_SIZE)
    else:
        df_sample = df.copy()

    df_main_cols = df_sample[['tweet_id', 'text']].copy(deep=True)
    df_main_cols.loc[:, 'sentiment'] = ''
    df_main_cols.loc[:, 'labels'] = ''
    df_main_cols.loc[:, 'ca_related'] = ''

    file_name = os.path.split(OUT_FILE_FILTERED_CSV)[-1].split('.')[0]
    append_to_csv(df_main_cols, 'data/annotated/' + file_name + '.csv')

if __name__ == '__main__':
    print()
    # November 29 collected - no prefix
    # for i in [2, 3]:
    #     print(f"\nUsing filter type [{i}]")
    #     main(i, '')

    # for i in [(1, 'key words channel')]:
    # for i in [(2, 'news_cannels'), (3, 'official organisations channel')]:
    #     print(f"\nUsing filter type - {i}")
    #     main(i[0], 'nov_30_')

    # for i in [(1, 'key words channel')]:
    # for i in [(2, 'news_cannels'), (3, 'official organisations channel')]:
    #     print(f"\nUsing filter type [{i}]")
    #     main(i[0], 'dec_01_')
