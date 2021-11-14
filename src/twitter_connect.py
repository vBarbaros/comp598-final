import requests
import os
import json

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

OUT_FILE = 'data/twitter_dump.json'

parentdir = Path(__file__).parents[1]

TWITTER_SEARCH_URL = 'https://api.twitter.com/2/tweets/search/recent'

SEARCH_QUERY_PARAMS = {
    'query': 'covid, moderna, vaccine (#moderna, OR #antivax) lang:en',
    'max_results': 100,
    'tweet.fields': 'author_id,created_at,entities,geo,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,source',
    'user.fields': 'created_at,entities'
}


def bearer_oauth_search(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = 'v2RecentSearchPythonComp598McGill'
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth_search, params=params)
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
    f.write(json.dumps(tmp_dict) + '\n')
    f.close()


def main():
    json_response = connect_to_endpoint(TWITTER_SEARCH_URL, SEARCH_QUERY_PARAMS)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    append_to_file(json_response['data'], out_file=OUT_FILE)


if __name__ == '__main__':
    main()
