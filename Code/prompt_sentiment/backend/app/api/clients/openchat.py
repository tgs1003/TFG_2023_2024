import requests
import json
import os
import logging
import six

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True)

api_key = os.getenv('HUGGINGFACE_API_KEY')
HUGGINGFACE_API_URL = os.getenv('HUGGINGFACE_API_URL')
headers = {"Authorization": "Bearer " + api_key}

class OpenChatSentimentAnalyzer():
    def get_sentiment(self, review_text):
        prompt_template = 'Return a json with the following information extracted from the review below you can find the review between triple backticks: \
{ \
"Sentiment": "(Positive or Negative)",\
"Stars": "Number of stars depending on the sentiment of the Review",\
"Anger": "Is the user angry (True or False)", \
} \
Review: ```' + \
review_text + \
'``` \
If the information is not present, use "unknown" as the value. \
Remember to return only the json. \
'
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json={"inputs": prompt_template})
        return self.parse_response(response.json())

    def parse_response(self, response):
        if type(response) == dict:
            if response.keys().__contains__("generated_text"):
                return self.parse_response(response["generated_text"])
            if response.keys().__contains__("choices"):
                return self.parse_response(response["choices"][0])
            elif response.keys().__contains__("text"):
                return self.parse_response(response["text"])
            else:
                return response
        if type(response) == list:
             return self.parse_response(response[0])
        if isinstance(response, six.string_types):
            try:
                return json.loads(self.clean_response(response))
            except:
                return None

    def clean_response(self, response):
        response = '\n'.join(response.split('\n')[1:])
        start = response.find("{")
        end = response.rfind("}") + 1
        temp = response[start:end]
        temp = temp.replace("'", '"')
        temp = temp.replace(": False,", ': "False",')
        temp = temp.replace(": True,", ': "True",')
        return temp

