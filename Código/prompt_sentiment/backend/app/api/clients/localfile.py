import pandas as pd
import logging
import os
import json
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

def load_dataset(dataset_id, path, n_rows):
    '''
    Carga un dataset en la base de datos para ser procesado.
    '''
    dataset1 = get_dataset_by_id(dataset_id)
    if dataset1 is None:
        raise Exception("El dataset no existe.")

    configuration = json.loads(config)
    path=configuration["path"]
    mapping = configuration["mapping"]

    correct_stars = 0
    if 'correct_stars' in configuration.keys():
        correct_stars=int(configuration["correct_stars"])
    
    date_format = ''
    if 'date_format' in configuration.keys():
        date_format=configuration["date_format"]

    review_text_fieldname = mapping['review_text']
    
    df = pd.read_csv(path)
    df = df.sample(frac=(sample/100))
    df.reset_index(drop=True, inplace=True)
    
    if 'review_headline' in mapping.keys():
        review_headline_fieldname = mapping['review_headline']
        df['review'] = df[review_headline_fieldname] + ". " + df[review_text_fieldname]
    else:
        df['review'] = df[review_text_fieldname]

    if 'stars' in mapping.keys():
        df['star_rating'] = df[mapping['stars']] + correct_stars

    df['prediction'] = None

    for i in range(df.shape[0]):
        product_id = "Unknown"
        if 'product_id' in mapping.keys():
            product_id = df.at[i, mapping['product_id']]
            product1 = get_product_by_id(product_id)
            if product1 is None:
                product_title = ""
                if 'product_title' in mapping.keys():
                    product_title_fieldname = mapping['product_title']
                    product_title = df.at[i, product_title_fieldname]
                else:
                    product_title = "Producto " + str(product_id)
                add_product(product_id, product_title)

        reviewer_id = 1
        if 'customer_id' in mapping.keys():
            reviewer_id = df.at[i, mapping['customer_id']]
            reviewuser1 = get_reviewuser_by_id(reviewer_id)
            if reviewuser1 is None:
                customer_name = ""
                if 'customer_name' in mapping.keys():
                    customer_name_fieldname = mapping['customer_name']
                    customer_name = df.at[i, customer_name_fieldname]
                else:
                    customer_name = "Usuario " + str(reviewer_id)
                
                add_reviewuser(reviewer_id, customer_name)
       
        review_id = ''
        if 'review_id' in mapping.keys():
            review_id = df.at[i,mapping['review_id']]
        
        review_date = str(datetime.now())
        if 'review_date' in mapping.keys():
            review_date = str(datetime.strptime(df.at[i,mapping['review_date']], date_format))

        review1 = get_review_by_dataset_id_and_review_id(dataset_id = dataset_id, review_id = review_id)
        
        if review1 is None:
            add_review(datasetId=dataset_id, 
                    originalId=review_id, 
                    productId=product_id, 
                    reviewText=df.at[i, 'review'], 
                    reviewTime=review_date, 
                    reviewerId=str(reviewer_id), 
                    stars=str(df.at[i,'star_rating']))
        else:
            logging.error(f"Reseña duplicada: DatasetId: {dataset_id} ReviewId: {review_id}")

load_dataset(1, )
