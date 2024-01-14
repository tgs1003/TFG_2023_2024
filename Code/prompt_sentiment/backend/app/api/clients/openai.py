import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True)

openai.api_key  = os.getenv('OPENAI_API_KEY')

llm_model = "gpt-3.5-turbo"
sentiment_schema = ResponseSchema(name="Sentiment",description="It's the sentiment of the review (positive or negative)")
anger_schema = ResponseSchema(name="Anger", description="Is the reviewer expressing anger? (true or false)")
stars_schema = ResponseSchema(name="Stars", description="Is a number between 1 and 5 indicating the rating of the review")
response_schemas = [sentiment_schema,
                    anger_schema,
                    stars_schema]
'''
Plantilla para identificar los sentimientos de una reseña.
Además intenta identificar otros elementos como el objeto de la reseña, el idioma y el fabricante.
'''
template_string ="""Return a json with the following information extracted from the review below: \
    {{ \
        ""Sentiment"": ""(positive or negative)"",\
        ""Stars"": ""Number of stars depending on the sentiment of the Review"",\
        ""Anger"": ""Is the user angry? (true or false)"", \
    }} \
Review: ```{review}``` \
If the information isn't present, use ""unknown"" as the value. \
Remember to return only the json. 
"""
chat = ChatOpenAI(temperature=0.0, model=llm_model, verbose=True)

class LangchainOpenAISentimentAnalyzer():
    def get_sentiment(self, review):
        prompt_template = ChatPromptTemplate.from_template(template_string)
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        prompt = prompt_template.format_messages(
        review = review, format_instructions=format_instructions)
        response = chat(prompt)
        return output_parser.parse(response.content)
