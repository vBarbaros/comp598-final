from dotenv.main import find_dotenv
import requests
import os
import json
import pandas as pd

from dotenv import load_dotenv
from pathlib import Path



load_dotenv(find_dotenv())
TWITTER_SEARCH_URL = 'https://api.twitter.com/2/tweets/search/recent'
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

OUT_FILE_JSON = 'data/twitter_dump_replies.json'
OUT_FILE_CSV = 'data/twitter_dump_replies.csv'

parentdir = Path(__file__).parents[1]


# 'query': 'covid, covid-19, covid19, moderna, vaccine, pfizer, Pfizer, Moderna, JohnsonAndJohnson, COVID19vaccine (#moderna, OR #pfizer, OR #covid, OR #covid19vaccine, OR #antivax) lang:en -is:retweet -is:reply',

# q: covid, moderna, vaccine (#moderna, OR #antivax) (@Canada) min_replies:10 lang:en until:2021-11-14 since:2021-11-13
# vaccine vaccination (pfzier OR moderna OR JohnsonAndJohnson)  (@CBCNews OR @JustinTrudeau) lang:en is:reply',

def bearer_oauth_search(r):
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = 'v2RecentSearchPythonComp598McGill'
    return r


def connect_to_endpoint(url, next_token=None):
    SEARCH_QUERY_PARAMS = {
        #'query': 'covid, moderna, vaccine (#moderna, OR #antivax) lang:en -is:rtwet -is:reply',
        # (Pfizer OR moderna OR vaccine OR vaccination) (@CBCNews OR @JustinTrudeau) lang:en filter:replies
        #'query': 'vaccine (pfzier OR moderna OR JohnsonAndJohnson) (#covid) (@CBCNews OR @JustinTrudeau) lang:en is:reply',
        #'query': 'vaccine (pfzier OR moderna OR JohnsonAndJohnson)  (@CBCNews OR @JustinTrudeau) lang:en is:reply',
        'query': 'vaccine (pfzier OR moderna OR JohnsonAndJohnson OR vaccine OR vaccination)(@CBCNews OR @JustinTrudeau OR @CBCCanada OR @CdnPressNews OR @GovCanHealth or @CBCAlerts) lang:en is:reply',
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


def append_to_file(tmp_dict, out_file):
    sample_file = os.path.join(parentdir, out_file)

    out_dir = os.path.split(sample_file)
    if not os.path.isdir(out_dir[0]):
        os.makedirs(out_dir[0])

    f = open(sample_file, 'a')
    f.write(json.dumps(tmp_dict, indent = 4) + '\n')
    f.close()


def read_from_csv_collected_tweets():
    sample_file = os.path.join(parentdir, OUT_FILE_CSV)
    if not os.path.exists(sample_file):
        return None

    df = pd.read_csv(sample_file)
    return df


def write_to_csv_collected_tweets(dataframe):
    sample_file = os.path.join(parentdir, OUT_FILE_CSV)
    dataframe.to_csv(sample_file, index=False)

def check_word_in_text(text):
    word_list = text.split()
    number = len(word_list)

    return number 

def main():
    previous_data_frame = read_from_csv_collected_tweets()
    if previous_data_frame is None:
        COLLECTED_TWEETS = []
    else:
        COLLECTED_TWEETS = previous_data_frame.values.tolist()

    json_response = connect_to_endpoint(TWITTER_SEARCH_URL)
    json_response_data, json_response_next_token = get_response_components(json_response)

    COLLECTED_TWEETS = process_response(COLLECTED_TWEETS, json_response_data)

    while json_response_next_token:
        json_response = connect_to_endpoint(TWITTER_SEARCH_URL, json_response_next_token)
        json_response_data, json_response_next_token = get_response_components(json_response)

        COLLECTED_TWEETS = process_response(COLLECTED_TWEETS, json_response_data)

    columns = ['tweet_id', 'text', 'source', 'created_at', 'possibly_sensitive', 'author_id', 'places_type',
               'places_normalized_text', 'hashtags', 'lang']
    df = pd.DataFrame(COLLECTED_TWEETS, columns=columns)
    write_to_csv_collected_tweets(df)
    append_to_file(json_response['data'], out_file=OUT_FILE_JSON)


def get_response_components(json_response):
    try:
        json_response_data = json_response['data']
    except KeyError:
        json_response_data = []
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
            if check_word_in_text (tweet['text']) >=10:
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


if __name__ == '__main__':
    main()
