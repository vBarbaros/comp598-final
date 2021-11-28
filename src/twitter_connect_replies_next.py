import pandas as pd
from pandas import DataFrame
from difflib import SequenceMatcher
from pathlib import Path
import os 
from datetime import datetime
import json

parentdir = Path(__file__).parents[1]
OUT_FILE_JSON = 'data/twitter_dump_replies_filter.json'
OUT_FILE_CSV = 'data/twitter_dump_replies_filter.csv'

raw_sample_file = "../data/twitter_dump_replies.csv"




def check_word_in_text(text):
    word_list = text.split()
    number = len(word_list)

    return number 

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def write_to_csv_collected_tweets(dataframe):
    sample_file = os.path.join(parentdir, OUT_FILE_CSV)
    dataframe.to_csv(sample_file, index=False)


def today_record(twitter_data):
    for index, row in twitter_data.iterrows():
        time = datetime.strptime(row['created_at'],'%Y-%m-%dT%H:%M:%S.000Z')
        if time.date() != datetime.today().date():
            twitter_data=twitter_data.drop(index)
            
    #print(twitter_data)

    return twitter_data

def json_out(pd_dataframe):
    outlist=[]
    for  index, row in pd_dataframe.iterrows():
        tweet = dict()
        tweet['id'] = row ['tweet_id'],
        tweet['text']=row ['text'],
        tweet['source']=row ['source'],
        tweet['created_at']=row ['created_at'],
        tweet['possibly_sensitive']=row ['possibly_sensitive'],
        tweet['author_id']=row ['author_id'],
        tweet['places_type']=row ["places_type"],
        tweet['places_normalized_text']=row['places_normalized_text'],
        tweet['hashtags']=row['hashtags'],
        tweet['lang']=row['lang']
        outlist.append(tweet)
    sample_out_file = os.path.join(parentdir, OUT_FILE_JSON)
    with open(sample_out_file, 'w') as f:
        json.dump(outlist, f, indent = 4)

    return


def main():
    df = pd.read_csv(raw_sample_file)
    # get the tweets for today only
    df_today= today_record(df)
   
    df_small_reindex= df_today.reset_index(drop=True)
    df_final = pd.DataFrame()
   # if there are less than 10 words in the text or the similarity is greater than 0.6, drop it. 
    for index, row in df_small_reindex.iterrows():

        if check_word_in_text(row['text'])>10:
       
            if index < (len(df_small_reindex)-1) and similar(row['text'], df_small_reindex.iloc[index+1]['text']) <0.3:
            
                df_final=df_final.append(row, ignore_index=True)

    
    write_to_csv_collected_tweets(df_final)
    json_out(df_final)

    
        





if __name__ == '__main__':
    main()

