import os.path
from pathlib import Path

import pandas as pd

from twitter_collect import get_file_paths, read_from_csv_collected_tweets, append_to_csv

ACCEPTED_COLUMNS = ['text', 'label', 'sentiment', 'ca_related']
USE_FILTER = 3

parentdir = Path(__file__).parents[1]

def main(USE_FILTER, FILE_PREFIX):
    global OUT_FILE_JSON, OUT_FILE_CSV, OUT_FILE_FILTERED_CSV, OUT_FILE_FILTERED_JSON, SEARCH_QUERY
    OUT_FILE_JSON, OUT_FILE_CSV, OUT_FILE_FILTERED_CSV, OUT_FILE_FILTERED_JSON, SEARCH_QUERY = get_file_paths(
        USE_FILTER, FILE_PREFIX)

    file_name = os.path.split(OUT_FILE_FILTERED_CSV)[-1].split('.')[0]
    annotated_file_name = 'data/annotated/' + file_name + '.csv'
    annotated_done_file_name = 'data/annotated/done/' + file_name + '.csv'

    df = read_from_csv_collected_tweets(annotated_file_name)
    df_annotated_so_far = read_from_csv_collected_tweets(annotated_done_file_name)
    if df_annotated_so_far is None:
        df_annotated_so_far = pd.DataFrame(columns=ACCEPTED_COLUMNS)

    df_annotated_data_list = []
    for i, row in df.iterrows():
        if row['text'] in df_annotated_so_far['text'].to_list():
            tmp_row = df_annotated_so_far.loc[df_annotated_so_far['text'] == row['text']]
            print(f"\nPREVIOUSLY LABELED")
            print('=====================================\n', tmp_row['text'].values[0], '\n=====================================')
            print(f"label - [ {tmp_row['label'].values[0]} ], sentiment - [ {tmp_row['sentiment'].values[0]} ], ca_related - [ {tmp_row['ca_related'].values[0]} ]")
            print('=====================================', '\n=====================================')
            rewrite = input('\nIf you want to rewrite labels enter \'z\' and hit ENTER: ')
            if rewrite == 'z':
                print('=====================================\n', tmp_row['text'].values[0],
                      '\n=====================================\n')
                label = input('Provide a Label and hit ENTER: ')
                sentiment = input('\nProvide a sentiment and hit ENTER: ')
                ca_related = input('\nProvide a ca_related flag and hit ENTER: ')
                df_annotated_so_far.at[tmp_row.index, 'label'] = label
                df_annotated_so_far.at[tmp_row.index, 'sentiment'] = sentiment
                df_annotated_so_far.at[tmp_row.index, 'ca_related'] = ca_related
                print()
        else:
            print('\nTweed ID: ', row['tweet_id'])
            print('=====================================\n', row['text'], '\n=====================================\n')
            label = input('Provide a Label and hit ENTER: ')
            sentiment = input('\nProvide a sentiment and hit ENTER: ')
            ca_related = input('\nProvide a ca_related flag and hit ENTER: ')

            print(f"\n You just labeled the tweet")
            print('\n=====================================\n', row['text'], '\n=====================================')
            print(f"label - [ {label} ], sentiment - [ {sentiment} ], ca_related - [ {ca_related} ]\n")
            print(f"...saving and going to the next tweet...\n")
            print('\n=====================================', '\n=====================================')

            df_annotated_data_list.append((row['text'], label, sentiment, ca_related))

    if len(df_annotated_data_list) != 0:
        df_from_list = pd.DataFrame(df_annotated_data_list, columns=ACCEPTED_COLUMNS)
        append_to_csv(df_from_list, annotated_done_file_name)
    else:
        append_to_csv(df_annotated_so_far, annotated_done_file_name)

if __name__ == '__main__':
    # November 29 collected - no prefix
    main(1, '')
    # main(2, '')
    # main(3, '')

    # for i in [(1, 'key words channel')]:
    # for i in [(2, 'news_cannels'), (3, 'official organisations channel')]:
    #     print(f"\nUsing filter type - {i}")
    #     main(i[0], 'nov_30_')

    # for i in [(1, 'key words channel')]:
    # for i in [(2, 'news_cannels'), (3, 'official organisations channel')]:
    #     print(f"\nUsing filter type [{i}]")
    #     main(i[0], 'dec_01_')
