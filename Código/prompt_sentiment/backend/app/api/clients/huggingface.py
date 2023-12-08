import pandas as pd
import logging
import os
import json
from huggingface_hub import hf_hub_download
from datasets import load_dataset
from datetime import datetime
from app.api.services.datasets import get_dataset_by_id
from app.api.services.products import get_product_by_id, add_product
from app.api.services.review_users import get_reviewuser_by_id, add_reviewuser
from app.api.services.reviews import get_review_by_dataset_id_and_review_id, add_review


logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

def load_dataset(dataset_id, config, sample):
    '''
    Carga un dataset en la base de datos para ser procesado.
    '''
    #config["path"]
    #config["subset"] # train, test
    #config["mapping"] # review_text, review_headline, stars, product_id, product_title, customer_id, review_id, review_date
    #config["correct_stars"] = 1 #suma 1
    #config["date_format"] = '%Y-%m-%d'
    dataset = load_dataset(config)
    subset = dataset["train"].to_iterable_dataset()
    df = pd.json_normalize(subset)
    df = df.sample(frac=(sample/100))
    df.reset_index(drop=True, inplace=True)
    df['review'] = df['review_headline'] + ". " + df['text']
    df['star_rating'] = df['labels'] + 1
    df['prediction'] = None
    dataset1 = get_dataset_by_id(dataset_id)
    if dataset1 is None:
        raise Exception("El dataset no existe.")

    for i in range(df.shape[0]):
        product_id = df.at[i, 'product_id']
        product1 = get_product_by_id(product_id)
        if product1 is None:
            add_product(product_id, df.at[i, 'product_title'])
        
        reviewer_id = df.at[i, 'customer_id']
        reviewuser1 = get_reviewuser_by_id(reviewer_id)
        if reviewer_id is None:
            add_reviewuser(reviewer_id, "Amazon user " + reviewer_id)
        review_id = df.at[i,'review_id']
        review1 = get_review_by_dataset_id_and_review_id(dataset_id = dataset_id, review_id = review_id)
        if review1 is None:
            add_review(datasetId=dataset_id, 
                    originalId=df.at[i,'review_id'], 
                    productId=product_id, 
                    reviewText=df.at[i, 'review'], 
                    reviewTime=str(datetime.strptime(df.at[i, 'review_date'], '%Y-%m-%d')), 
                    reviewerId=str(reviewer_id), 
                    stars=str(df.at[i,'star_rating']))
        else:
            logging.error(f"Reseña duplicada: DatasetId: {dataset_id} ReviewId: {review_id}")
        
def download_model(repo_id, filename):
    hf_hub_download(repo_id, filename)

