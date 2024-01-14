import pandas as pd
import logging
import json
from huggingface_hub import hf_hub_download
from datasets import load_dataset as ld
from datetime import datetime
from app.api.services.datasets import get_dataset_by_id
from app.api.services.reviews import add_review


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
    dataset1 = get_dataset_by_id(dataset_id)
    if dataset1 is None:
        raise Exception("El dataset no existe.")

    configuration = json.loads(config)
    path=configuration["path"]
    subset_cfg=configuration["subset"]
    mapping = configuration["mapping"]

    correct_stars = 0
    if 'correct_stars' in configuration.keys():
        correct_stars=int(configuration["correct_stars"])

    date_format = ''
    if 'date_format' in configuration.keys():
        date_format=configuration["date_format"]

    review_text_fieldname = mapping['review_text']
    
    dataset = ld(path)
    subset = dataset[subset_cfg].to_iterable_dataset()
    df = pd.json_normalize(subset)
    df = df.sample(frac=(sample/100))
    df.reset_index(drop=True, inplace=True)
    
    if 'review_headline' in mapping.keys():
        review_headline_fieldname = mapping['review_headline']
        df['review'] = df[review_headline_fieldname] + ". " + df[review_text_fieldname]
    else:
        df['review'] = df[review_text_fieldname]

    if 'stars' in mapping.keys():
        df['star_rating'] = df[mapping['stars']] + correct_stars

    for i in range(df.shape[0]):
        review_date = str(datetime.now())
        if 'review_date' in mapping.keys():
            review_date = str(datetime.strptime(df.at[i,mapping['review_date']], date_format))
        add_review(dataset_id=dataset_id,   
                    review_text=df.at[i, 'review'], 
                    review_time=review_date, 
                    original_stars=str(df.at[i,'star_rating']))
        
def download_model(repo_id, filename):
    hf_hub_download(repo_id, filename)

