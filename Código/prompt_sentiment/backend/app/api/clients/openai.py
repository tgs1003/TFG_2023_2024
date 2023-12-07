import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True)

openai.api_key  = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_BASE_PATH')
llm_model = "gpt-3.5-turbo"
sentiment_schema = ResponseSchema(name="Sentiment",description="It's the sentiment of the review (positiva or negative)")
anger_schema = ResponseSchema(name="Anger", description="Is the reviewer expressing anger? (true or false)")
item_schema = ResponseSchema(name="Item", description="Item purchaded by the reviewer")
company_schema = ResponseSchema(name="Brand", description="Company that made the item")
language_schema = ResponseSchema(name="Language", description="The language of the review")
stars_schema = ResponseSchema(name="Stars", description="The rating of the review being 1 most negative and 5 the most positive")
response_schemas = [sentiment_schema, 
                    anger_schema,
                    item_schema,
                    company_schema,
                    language_schema,
                    stars_schema
                    ]
'''
Plantilla para identificar los sentimientos de una reseña.
Además intenta identificar otros elementos como el objeto de la reseña, el idioma y el fabricante.
'''
template_string ="""Identify the following items from the review text: \
- Sentiment (positive or negative) \
- Is the reviewer expressing anger? (true or false) \
- Item purchased by reviewer \
- Company that made the item \
- Language \
- Stars
\
The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Anger", "Item" ,"Brand", "Language" and "Stars" as the keys. \
If the information isn\'t present, use "unknown" \
as the value.\
Make your response as short as possible.\
Format the Anger value as a boolean.\
Format the Language value as ISO 639-1.\
\
Review text: \'\'\'{text}\'\'\''
"""
chat = ChatOpenAI(temperature=0.0, model=llm_model, verbose=True)

class LangchainOpenAISentimentAnalyzer():
    def get_sentiment(self, text):
        prompt_template = ChatPromptTemplate.from_template(template_string)
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        prompt = prompt_template.format_messages(
        text = text)
        response = chat(prompt)
        
        return output_parser.parse(response.content)
