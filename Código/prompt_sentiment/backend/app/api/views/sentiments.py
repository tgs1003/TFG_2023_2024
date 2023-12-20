from flask import request
from flask_restx import Resource, fields, Namespace
from app.api.services.tokens import check_token
from app.api.services.roles import user_has_rol
from app.api.services.sentiments import(
    get_all_sentiments,
    get_sentiment_by_id,
    add_sentiment,
    update_sentiment,
    delete_sentiment,
    get_old_sentiment,
)

sentiments_namespace = Namespace("sentiments")
put_parser = sentiments_namespace.parser()
put_parser.add_argument("Authorization", location="headers")
put_parser.add_argument("review_id", location="json")
put_parser.add_argument("stars", location="json")
put_parser.add_argument("sentiment", location="json")
put_parser.add_argument("anger", location="json")
put_parser.add_argument("item", location="json")
put_parser.add_argument("brand", location="json")
put_parser.add_argument("language", location="json")
put_parser.add_argument("source", location="json")
put_parser.add_argument("model", location="json")
put_parser.add_argument("correct", location="json")
put_parser.add_argument("process_time", location="json")
put_parser.add_argument("tokens", location="json")

parser = sentiments_namespace.parser()
parser.add_argument("Authorization", location="headers")

sentiments = sentiments_namespace.model(
    "Sentiment",
    {
        "review_id": fields.Integer(required=True),
        "stars": fields.Integer,
        "sentiment": fields.String,
        "anger": fields.Boolean,
        "item": fields.String,
        "brand": fields.String,
        "language": fields.String,
        "source": fields.String,
        "model": fields.String(required=True),
        "correct": fields.Boolean(required=True),
        "process_time": fields.Integer,
        "tokens": fields.Integer
    },
)
sentiments_put = sentiments_namespace.model(
    "Sentiment put",
    {
        "id": fields.Integer(readOnly=True),
        "correct": fields.Boolean(required=True),
    })


class SentimentList(Resource):
    @sentiments_namespace.marshal_with(sentiments, as_list=True)
    @sentiments_namespace.expect(parser)
    def get(self):
        """Devuelve todos los sentimientos de las reseñas."""
        check_token(request, sentiments_namespace)
        return get_all_sentiments(), 200
        
    @sentiments_namespace.marshal_with(sentiments)
    @sentiments_namespace.response(201, "El sentimiento para la reseña <reviewId> se ha agregado.")
    @sentiments_namespace.response(400, "El sentimiento ya existe.")
    @sentiments_namespace.expect(parser)
    def post(self):
        """Crea un sentimiento."""
        if not user_has_rol(request, "Admin", sentiments_namespace):
            sentiments_namespace.abort(403, "El usuario no es administrador.")
        post_data = request.get_json()
        review_id = post_data.get("review_id")
        stars = post_data.get("stars")
        sentiment = post_data.get("sentiment")
        anger = post_data.get("anger")
        source = post_data.get("source")
        model = post_data.get("model")
        correct = post_data.get("correct")
        process_time = post_data.get("process_time")
        tokens = post_data.get("tokens")
        response_object = {}

        sentiment_analysis = get_old_sentiment(review_id, model)
        if sentiment_analysis:
            response_object["message"] = "El sentimiento ya existe."
            return response_object, 400
        
        sent = add_sentiment(review_id = review_id, stars = stars, 
                      sentiment = sentiment, anger = anger,
                        source=source, model=model, 
                      correct=correct, process_time = process_time, tokens = tokens
                      )
        response_object["message"] = f"Se ha añadido el sentimento para la reseña {review_id}."
        return response_object, 201

class Sentiments(Resource):
    @sentiments_namespace.marshal_with(sentiments)
    @sentiments_namespace.response(200, "Correcto")
    @sentiments_namespace.response(404, "El sentimiento <sentiment_id> no existe.")
    @sentiments_namespace.expect(parser)
    def get(self, sentiment_id):
        """Devuelve un sentimiento."""
        check_token(request, sentiments_namespace)
        sentiment = get_sentiment_by_id(sentiment_id)
        if not sentiment:
            sentiments_namespace.abort(404, f"El sentimiento {sentiment_id} no existe.")
        return sentiment, 200

    @sentiments_namespace.expect(put_parser, validate=True)
    @sentiments_namespace.response(200, "Sentimento <sentiment_id> actualizado.")
    @sentiments_namespace.response(404, "El sentimiento <sentiment_id> no existe.")
    def put(self, sentiment_id):
        """Actualiza un sentimiento."""
        if not user_has_rol(request, "Admin", sentiments_namespace):
            sentiments_namespace.abort(403, "El usuario no es administrador.")
        post_data = request.get_json()
        correct = post_data.get("correct")
        response_object = {}
        sentiment = get_sentiment_by_id(sentiment_id)
        if not sentiment:
            sentiments_namespace.abort(404, f"El sentimiento {sentiment_id} no existe.")
        update_sentiment(sentiment, correct)
        response_object["message"] = f"Sentimiento {sentiment.id} actualizado."
        return response_object, 200

    @sentiments_namespace.response(200, "Sentimiento <sentiment_id> eliminado.")
    @sentiments_namespace.response(404, "El sentimiento <sentiment_id> no existe.")
    @sentiments_namespace.expect(parser)
    def delete(self, sentiment_id):
        """Borra un sentimiento."""
        if not user_has_rol(request, "Admin", sentiments_namespace):
            sentiments_namespace.abort(403, "El usuario no es administrador.")
        response_object = {}
        sentiment = get_sentiment_by_id(sentiment_id)
        if not sentiment:
            sentiments_namespace.abort(404, f"El sentimiento {sentiment_id} no existe.")
        delete_sentiment(sentiment)
        response_object["message"] = f"El sentimiento {sentiment.id} se ha borrado."
        return response_object, 200

#
sentiments_review = sentiments_namespace.model(
    "SentimentReview",
    {
        "dataset_id": fields.Integer,
        "id": fields.Integer,
        "stars": fields.Integer,
        "sentiment": fields.String,
        "original_stars": fields.Integer,
        "review_text": fields.String,
        "model": fields.String,
        "process_time": fields.Integer,
        "tokens": fields.Integer,
    },
)

sentiments_namespace.add_resource(SentimentList, "")
sentiments_namespace.add_resource(Sentiments, "/<int:sentiment_id>")