import os
from huggingface_hub import hf_hub_download

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

model_path = os.environ.get("MODEL_PATH")
model_basename = os.environ.get("MODEL_BASENAME")

hf_hub_download(repo_id=model_path, filename=model_basename,)