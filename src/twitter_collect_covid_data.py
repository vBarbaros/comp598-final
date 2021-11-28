from dotenv.main import find_dotenv
import requests
import os
import json
import pandas as pd

from dotenv import load_dotenv
from pathlib import Path

from src.twitter_preprocess_functions import today_record, collect_valid_tweets

load_dotenv(find_dotenv())
TWITTER_SEARCH_URL = 'https://api.twitter.com/2/tweets/search/recent'
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

TWEET_THRESHOLD = 12000
USE_FILTER = 3

if USE_FILTER == 1:
    OUT_FILE_JSON = 'data/twitter_dump_by_keywords.json'
    OUT_FILE_CSV = 'data/twitter_dump_by_keywords.csv'
    OUT_FILE_FILTERED_CSV = 'data/processed/twitter_dump_by_keywords_filtered.csv'
    OUT_FILE_FILTERED_JSON = 'data/processed/twitter_dump_by_keywords_filtered.json'
    SEARCH_QUERY = 'vaccine (pfzier OR moderna OR JohnsonAndJohnson OR vaccine OR vaccination) lang:en -is:retweet -is:reply'
elif USE_FILTER == 2:
    OUT_FILE_JSON = 'data/twitter_dump_replies_cbc_only.json'
    OUT_FILE_CSV = 'data/twitter_dump_replies_cbc_only.csv'
    OUT_FILE_FILTERED_CSV = 'data/processed/twitter_dump_replies_cbc_only_filtered.csv'
    OUT_FILE_FILTERED_JSON = 'data/processed/twitter_dump_replies_cbc_only_filtered.json'
    SEARCH_QUERY = 'vaccine (pfzier OR moderna OR JohnsonAndJohnson OR vaccine OR vaccination) (@CBCNews OR @CBCCanada OR @CdnPressNews OR @CBCAlerts) lang:en is:reply'
elif USE_FILTER == 3:
    OUT_FILE_JSON = 'data/twitter_dump_replies_gvnmt_only.json'
    OUT_FILE_CSV = 'data/twitter_dump_replies_gvnmt_only.csv'
    OUT_FILE_FILTERED_CSV = 'data/processed/twitter_dump_replies_gvnmt_only_filtered.csv'
    OUT_FILE_FILTERED_JSON = 'data/processed/twitter_dump_replies_gvnmt_only_filtered.json'
    SEARCH_QUERY = 'vaccine (pfzier OR moderna OR JohnsonAndJohnson OR vaccine OR vaccination) (@CanBorder OR @JustinTrudeau OR @TravelGoC OR @CPHO_Canada OR @GovCanHealth or @CanadianPM or @Safety_Canada) lang:en is:reply'

parentdir = Path(__file__).parents[1]


def bearer_oauth_search(r):
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = 'v2RecentSearchPythonComp598McGill'
    return r


def connect_to_endpoint(url, next_token=None):
    SEARCH_QUERY_PARAMS = {
        'query': SEARCH_QUERY,
        'max_results': 100,
        'tweet.fields': 'author_id,created_at,entities,geo,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,source',
        'user.fields': 'created_at,entities'
    }
    if next_token:
        SEARCH_QUERY_PARAMS['next_token'] = next_token

    response = requests.request("GET", url, auth=bearer_oauth_search, params=SEARCH_QUERY_PARAMS)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def append_to_json(tmp_dict, out_file):
    sample_file = os.path.join(parentdir, out_file)

    out_dir = os.path.split(sample_file)
    if not os.path.isdir(out_dir[0]):
        os.makedirs(out_dir[0])

    f = open(sample_file, 'a')
    f.write(json.dumps(tmp_dict, indent=4) + '\n')
    f.close()


def read_from_csv_collected_tweets():
    sample_file = os.path.join(parentdir, OUT_FILE_CSV)
    if not os.path.exists(sample_file):
        return None

    df = pd.read_csv(sample_file)
    return df


def append_to_csv(dataframe, out_file_csv):
    sample_file = os.path.join(parentdir, out_file_csv)
    dataframe.to_csv(sample_file, index=False)


def get_tweets_dataframe(COLLECTED_TWEETS):
    columns = ['tweet_id', 'text', 'source', 'created_at', 'possibly_sensitive', 'author_id', 'places_type',
               'places_normalized_text', 'hashtags', 'lang']
    return pd.DataFrame(COLLECTED_TWEETS, columns=columns)


def check_word_in_text(text):
    word_list = text.split()
    number = len(word_list)

    return number


def get_response_components(json_response):
    try:
        json_response_data = json_response['data']
    except KeyError:
        json_response_data = None

    try:
        json_response_next_token = json_response['meta']['next_token']
    except KeyError:
        json_response_next_token = None
    return json_response_data, json_response_next_token


def process_response(COLLECTED_TWEETS, json_response_data):
    for tweet in json_response_data:
        unique_ids = [str(t[0]) for t in COLLECTED_TWEETS]
        tweet_already_collected = tweet['id'] in unique_ids
        if not tweet_already_collected:
            places_type, places_normalized_text, hashtags = None, None, None
            try:
                places_type = ' '.join([tag_dict['type'] for tag_dict in tweet['entities']['annotations']])
            except:
                pass

            try:
                places_normalized_text = ' '.join(
                    [tag_dict['normalized_text'] for tag_dict in tweet['entities']['annotations']])
            except:
                pass

            try:
                hashtags = ' '.join([tag_dict['tag'] for tag_dict in tweet['entities']['hashtags']])
            except:
                pass
            if check_word_in_text(tweet['text']) >= 10:
                COLLECTED_TWEETS.append(
                    [
                        tweet['id'],
                        tweet['text'],
                        tweet['source'],
                        tweet['created_at'],
                        tweet['possibly_sensitive'],
                        tweet['author_id'],
                        places_type,
                        places_normalized_text,
                        hashtags,
                        tweet['lang']
                    ]
                )

    return COLLECTED_TWEETS


def collect_new_tweets(COLLECTED_TWEETS, json_response_next_token=None):
    json_response = connect_to_endpoint(TWITTER_SEARCH_URL, json_response_next_token)
    json_response_data, json_response_next_token = get_response_components(json_response)
    COLLECTED_TWEETS = process_response(COLLECTED_TWEETS, json_response_data)
    return COLLECTED_TWEETS, json_response, json_response_next_token


def get_collected_tweets():
    previous_data_frame = read_from_csv_collected_tweets()
    if previous_data_frame is None:
        COLLECTED_TWEETS = []
    else:
        COLLECTED_TWEETS = previous_data_frame.values.tolist()
    return COLLECTED_TWEETS


def append_to_files_all(tweet_data, dict_data, out_file_csv, out_file_json):
    dataframe = get_tweets_dataframe(tweet_data)
    append_to_csv(dataframe, out_file_csv)
    if dict_data is not None:
        append_to_json(dict_data, out_file=out_file_json)


def collect(COLLECTED_TWEETS):
    COLLECTED_TWEETS, json_response, json_response_next_token = collect_new_tweets(COLLECTED_TWEETS)
    while json_response_next_token:
        COLLECTED_TWEETS, json_response, json_response_next_token = collect_new_tweets(COLLECTED_TWEETS,
                                                                                       json_response_next_token)
        if len(COLLECTED_TWEETS) > TWEET_THRESHOLD:
            break
    return COLLECTED_TWEETS, json_response


def preprocess_collected_tweets():
    sample_file = os.path.join(parentdir, OUT_FILE_CSV)
    df = pd.read_csv(sample_file)
    df_today = today_record(df)
    df_small_reindex = df_today.reset_index(drop=True)
    COLLECTED_TWEETS_PROCESSED = collect_valid_tweets(df_small_reindex)
    return COLLECTED_TWEETS_PROCESSED


def main():
    COLLECTED_TWEETS = get_collected_tweets()

    COLLECTED_TWEETS, json_response = collect(COLLECTED_TWEETS)
    append_to_files_all(COLLECTED_TWEETS, None, OUT_FILE_CSV, OUT_FILE_JSON)

    COLLECTED_TWEETS_PROCESSED = preprocess_collected_tweets()
    append_to_files_all(COLLECTED_TWEETS_PROCESSED, None, OUT_FILE_FILTERED_CSV, OUT_FILE_FILTERED_JSON)


if __name__ == '__main__':
    main()
