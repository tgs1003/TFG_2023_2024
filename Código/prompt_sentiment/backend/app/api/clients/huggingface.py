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
    configuration = json.loads(config)
    path=configuration["path"]
    subset_cfg=configuration["subset"]
    mapping = configuration["mapping"]
    correct_stars=int(configuration["correct_stars"])
    date_format=configuration["date_format"]
    review_text_fieldname = mapping['review_text']
    stars_fieldname = mapping['stars']
    product_id_fieldname = mapping['product_id']
    customer_id_fieldname = mapping['customer_id']
    review_id_fieldname = mapping['review_id']
    review_date_fieldname = mapping['review_date']
    
    dataset = load_dataset(path)
    subset = dataset[subset_cfg].to_iterable_dataset()
    df = pd.json_normalize(subset)
    df = df.sample(frac=(sample/100))
    df.reset_index(drop=True, inplace=True)
    
    if 'review_headline' in mapping.keys():
        review_headline_fieldname = mapping['review_headline']
        df['review'] = df[review_headline_fieldname] + ". " + df[review_text_fieldname]
    else:
        df['review'] = df[review_text_fieldname]
        
    df['star_rating'] = df[stars_fieldname] + correct_stars
    df['prediction'] = None
    dataset1 = get_dataset_by_id(dataset_id)
    if dataset1 is None:
        raise Exception("El dataset no existe.")

    for i in range(df.shape[0]):
        product_id = df.at[i, product_id_fieldname]
        product1 = get_product_by_id(product_id)
        if product1 is None:
            product_title = ""
            if 'product_title' in mapping.keys():
                product_title_fieldname = mapping['product_title']
                product_title = df.at[i, product_title_fieldname]
            else:
                product_title = "Producto " + str(product_id)
            add_product(product_id, product_title)
        
        reviewer_id = df.at[i, customer_id_fieldname]
        reviewuser1 = get_reviewuser_by_id(reviewer_id)
        if reviewuser1 is None:
            customer_name = ""
            if 'customer_name' in mapping.keys():
                customer_name_fieldname = mapping['customer_name']
                customer_name = df.at[i, customer_name_fieldname]
            else:
                customer_name = "Usuario " + str(reviewer_id)
            
            add_reviewuser(reviewer_id, customer_name)
            
        review_id = df.at[i,review_id_fieldname]
        review1 = get_review_by_dataset_id_and_review_id(dataset_id = dataset_id, review_id = review_id)
        if review1 is None:
            add_review(datasetId=dataset_id, 
                    originalId=review_id, 
                    productId=product_id, 
                    reviewText=df.at[i, 'review'], 
                    reviewTime=str(datetime.strptime(df.at[i, review_date_fieldname], date_format)), 
                    reviewerId=str(reviewer_id), 
                    stars=str(df.at[i,'star_rating']))
        else:
            logging.error(f"Reseña duplicada: DatasetId: {dataset_id} ReviewId: {review_id}")
        
def download_model(repo_id, filename):
    hf_hub_download(repo_id, filename)

