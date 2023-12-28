import pandas as pd
import os
from datasets import load_dataset
from datetime import datetime
import logging
import requests
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

logging.basicConfig(level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])


def split_dataset(path, folder):
    dataset = load_dataset(path)
    train_dataset = dataset["train"].to_iterable_dataset()
    df = pd.json_normalize(train_dataset)
    df = df.filter(items=['product_id', 'text'])
    #df = df.sample(frac=sample)
    products = df.filter(items=['product_id']).drop_duplicates()
    products.reset_index(drop=True, inplace=True)
    for i in range(products.shape[0]):
        product_id = products.at[i, 'product_id']
        product_df = df[df['product_id'] == product_id].filter(items=['text'])
        product_df[df['product_id'] == product_id].to_json(folder + product_id + '.json', orient='records')
    #df.reset_index(drop=True, inplace=True)
    #df['review'] = df['review_headline'] + ". " + df['text']
    #df['star_rating'] = df['labels'] + 1
    #df['prediction'] = None
    
    #for i in range(df.shape[0]):
    #    asin = df.at[i, 'product_id']
    #    result_code, product1 = self.get_data("/products/" + asin)
    #    if result_code == 404:
    #        result_code, product1 = self.post_data("/products", 
    #                                    payload={
    #                                        "productId": asin, 
    #                                        "title": df.at[i, 'product_title']
    #                                    })
        
        
   
        
    
if __name__ == "__main__":
    split_dataset('mesmalif/amazon-shoe-reviews', '/tmp/promptsentiment/json/')