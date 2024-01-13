import pandas as pd
import logging
import json
from app.api.services.datasets import get_dataset_by_id
from app.api.services.reviews import add_review
from app.api.services.files import get_file


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
    config = config.replace("'", '"')
    configuration = json.loads(config)
    fileId = configuration["fileId"]
    fileFormat = configuration["fileFormat"]
    separator = configuration["separator"]
    reviewColumn = configuration["reviewColumn"]
    buffer = get_file(fileId)
    if fileFormat == "json":
        df = pd.read_json(buffer)
    elif fileFormat == "csv":
        df = pd.read_csv(buffer, sep = separator)
    df = df.sample(frac=(sample/100))
    df.reset_index(drop=True, inplace=True)
    for i in range(df.shape[0]):
        add_review(dataset_id=dataset_id,
        review_text=df.at[i, reviewColumn])
