import logging
import json
import time
from flask import request
from flask_restx import Resource, fields, Namespace
from app.api.services.datasets import get_all_datasets, get_dataset_by_config, get_dataset_by_id, update_dataset, delete_dataset, add_dataset
from app.api.services.reviews import count_reviews_by_dataset_id, get_reviews_by_dataset_id
from app.api.services.sentiments import count_sentiments_by_dataset_id, add_sentiment
from app.api.services.tokens import check_token
from app.api.services.roles import user_has_rol
from app.api.clients.huggingface import load_dataset
from app.api.clients.openai import LangchainOpenAISentimentAnalyzer

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

datasets_namespace = Namespace("datasets")

post_parser = datasets_namespace.parser()
post_parser.add_argument("Authorization", location="headers")
post_parser.add_argument("name", location="json", required=True)
post_parser.add_argument("type", location="json")
post_parser.add_argument("config", location="json")
post_parser.add_argument("owner", location="json")

put_parser = datasets_namespace.parser()
put_parser.add_argument("Authorization", location="headers")
put_parser.add_argument("status", location="json", required=True)

parser = datasets_namespace.parser()
parser.add_argument("Authorization", location="headers")

datasets = datasets_namespace.model(
"dataset",
    {
        "id": fields.Integer(readOnly=True),
        "name": fields.String,
        "type": fields.String,
        "config": fields.String,
        "status":fields.String,
        "date": fields.DateTime
    },
)
datasets_get = datasets_namespace.inherit(
    "Datasets get", datasets, {"total": fields.Integer, "processed": fields.Integer}
)
class DatasetList(Resource):
    @datasets_namespace.marshal_with(datasets_get, as_list=True)
    @datasets_namespace.expect(parser)
    def get(self):
        """Devuelve todos los datasets."""
        check_token(request, datasets_namespace)
        all_datsets = get_all_datasets()
        for dataset in all_datsets:
            dataset.total = count_reviews_by_dataset_id(dataset.id)
            dataset.processed = count_sentiments_by_dataset_id(dataset.id)
        return all_datsets, 200

    @datasets_namespace.response(201, "El dataset <dataset_name> se ha agregado.")
    @datasets_namespace.response(400, "El dataset ya existe.")
    @datasets_namespace.expect(post_parser, validate=True)
    def post(self):
        """Crea un dataset."""
        data = post_parser.parse_args(request)
        if not user_has_rol(request, "Admin", datasets_namespace):
            datasets_namespace.abort(403, "El usuario no es administrador.")
        name = data["name"]
        type = data["type"]
        config = data["config"]
        owner = data["owner"]
        response_object = {}
        # TODO: Comprobar si ya existe con nombre y tipo
        dataset = get_dataset_by_config(config)
        if dataset:
            response_object["message"] = "El dataset ya existe."
            return response_object, 400
        add_dataset(name = name, type = type, config = config, owner = owner)
        response_object["message"] = f"Se ha añadido el dataset {name}."
        return response_object, 201

class Datasets(Resource):
    @datasets_namespace.marshal_with(datasets_get)
    @datasets_namespace.response(200, "Correcto")
    @datasets_namespace.response(404, "El dataset <dataset_id> no existe.")
    @datasets_namespace.expect(parser)
    def get(self, dataset_id):
        """Devuelve una dataset."""
        check_token(request, datasets_namespace)
        dataset = get_dataset_by_id(dataset_id)
        if not dataset:
            datasets_namespace.abort(404, f"El dataset {dataset_id} no existe.")
        dataset.total = count_reviews_by_dataset_id(dataset_id)
        dataset.processed = count_sentiments_by_dataset_id(dataset_id)
        return dataset, 200

    
    @datasets_namespace.expect(put_parser, validate=True)
    @datasets_namespace.response(200, "Dataset <dataset_id> actualizado.")
    @datasets_namespace.response(404, "El dataset <dataset_id> no existe.")
    def put(self, dataset_id):
        """Actualiza un dataset."""
        data = put_parser.parse_args(request)
        if not user_has_rol(request, "Admin", datasets_namespace):
            datasets_namespace.abort(403, "El usuario no es administrador.")

        status = data["status"]
        response_object = {}
        dataset = get_dataset_by_id(dataset_id)
        if not dataset:
            datasets_namespace.abort(404, f"El dataset {dataset_id} no existe.")
        update_dataset(dataset, status)
        response_object["message"] = f"Dataset {dataset.id} actualizado."
        return response_object, 200
    
    @datasets_namespace.response(200, "Dataset <dataset_id> eliminado.")
    @datasets_namespace.response(404, "El dataset <dataset_id> no existe.")
    @datasets_namespace.expect(parser)
    def delete(self, dataset_id):
        """Borra un dataset."""
        if not user_has_rol(request, "Admin", datasets_namespace):
            datasets_namespace.abort(403, "El usuario no es administrador.")
        response_object = {}
        dataset = get_dataset_by_id(dataset_id)
        if not dataset:
            datasets_namespace.abort(404, f"El dataset {dataset_id} no existe.")
        delete_dataset(dataset)
        response_object["message"] = f"El dataset {dataset.id} se ha borrado."
        return response_object, 200
    
load_dataset_parser = datasets_namespace.parser()
put_parser.add_argument("Authorization", location="headers")
put_parser.add_argument("sample", location="json")
    
class DatasetLoad(Resource):
    '''
    Clase para gestionar la carga de los dataset
    '''
    @datasets_namespace.expect(load_dataset_parser, validate=True)
    @datasets_namespace.response(200, "El dataset <dataset_id> se ha enviado al proceso de carga.")
    @datasets_namespace.response(404, "El dataset <dataset_id> no existe.")
    def put(self, dataset_id):
        """Carga un dataset."""
        check_token(request, datasets_namespace)
        post_data = request.get_json()
        sample = post_data.get("sample")
        response_object = {}
        dataset = get_dataset_by_id(dataset_id)
        if not dataset:
            datasets_namespace.abort(404, f"El dataset {dataset_id} no existe.")
            
        load_dataset(dataset_id, dataset.payload, sample)
        response_object["message"] = f"Dataset {dataset.id} se ha cargado."
        return "Ok", 200
    
class DatasetProcess(Resource):
    @datasets_namespace.expect(parser, validate=True)
    @datasets_namespace.response(200, "Dataset <dataset_id> actualizado.")
    @datasets_namespace.response(404, "El dataset <dataset_id> no existe.")
    def put(self, dataset_id):
        """Procesa un dataset."""
        check_token(request, datasets_namespace)
        dataset = get_dataset_by_id(dataset_id)
        if not dataset:
            datasets_namespace.abort(404, f"El dataset {dataset_id} no existe.")
        response_object = {}
        
        openai = LangchainOpenAISentimentAnalyzer()
        reviews = get_reviews_by_dataset_id(dataset_id)
        for review_data in reviews:
            time_start = time.perf_counter()
            result = openai.get_sentiment(review_data.reviewText)
            review_id = review_data.id
            try:
                stars = self.parse_stars(result["Stars"])
                sentiment = result["Sentiment"]
                anger = result["Anger"]
                model = "OpenAI"
                process_time = int(time.perf_counter() - time_start)
                add_sentiment(reviewId=review_id, 
                            stars=int(stars), 
                            sentiment=sentiment, 
                            anger=bool(anger), 
                            model=model, 
                            correct=True,
                            process_time = process_time)
            except:
                add_sentiment(reviewId=review_id, 
                            correct=False,
                            model=model,
                            source=json.dumps(result),                            
                            process_time = process_time)

        response_object["message"] = f"Dataset {dataset.id} se ha procesado correctamente."
        return response_object, 200
    
    def parse_stars(self, stars):
        if type(stars) == int:
            return stars
        elif stars == 'Five':
            return 5
        elif stars == 'Four':
            return 4
        elif stars == 'Three':
            return 3
        elif stars == 'Two':
            return 2
        elif stars == 'One':
            return 1
        return stars

datasets_namespace.add_resource(DatasetList, "")
datasets_namespace.add_resource(Datasets, "/<int:dataset_id>")
datasets_namespace.add_resource(DatasetLoad, "/<int:dataset_id>/load")
datasets_namespace.add_resource(DatasetProcess, "/<int:dataset_id>/process")

