import pandas as pd

from datasets import load_dataset
import logging



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
    products = df.filter(items=['product_id']).drop_duplicates()
    products.reset_index(drop=True, inplace=True)
    for i in range(products.shape[0]):
        product_id = products.at[i, 'product_id']
        product_df = df[df['product_id'] == product_id].filter(items=['text'])
        product_df[df['product_id'] == product_id].to_json(folder + product_id + '.json', orient='records')

if __name__ == "__main__":
    split_dataset('mesmalif/amazon-shoe-reviews', '/tmp/promptsentiment/json/')