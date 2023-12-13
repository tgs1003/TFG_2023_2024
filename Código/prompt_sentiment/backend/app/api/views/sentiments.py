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
    get_sentiments_by_product_id,
    get_sentiments_by_reviewuser_id
)

sentiments_namespace = Namespace("sentiments")
put_parser = sentiments_namespace.parser()
put_parser.add_argument("Authorization", location="headers")
put_parser.add_argument("reviewId", location="json")
put_parser.add_argument("stars", location="json")
put_parser.add_argument("sentiment", location="json")
put_parser.add_argument("anger", location="json")
put_parser.add_argument("item", location="json")
put_parser.add_argument("brand", location="json")
put_parser.add_argument("language", location="json")
put_parser.add_argument("source", location="json")
put_parser.add_argument("model", location="json")
put_parser.add_argument("correct", location="json")
put_parser.add_argument("processTime", location="json")
put_parser.add_argument("tokens", location="json")

parser = sentiments_namespace.parser()
parser.add_argument("Authorization", location="headers")

sentiments = sentiments_namespace.model(
    "Sentiment",
    {
        "reviewId": fields.Integer(required=True),
        "stars": fields.Integer,
        "sentiment": fields.String,
        "anger": fields.Boolean,
        "item": fields.String,
        "brand": fields.String,
        "language": fields.String,
        "source": fields.String,
        "model": fields.String(required=True),
        "correct": fields.Boolean(required=True),
        "processTime": fields.Integer,
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
        reviewId = post_data.get("reviewId")
        stars = post_data.get("stars")
        sentiment = post_data.get("sentiment")
        anger = post_data.get("anger")
        item = post_data.get("item")
        brand = post_data.get("brand")
        language = post_data.get("language")
        source = post_data.get("source")
        model = post_data.get("model")
        correct = post_data.get("correct")
        processTime = post_data.get("processTime")
        tokens = post_data.get("tokens")
        response_object = {}

        sentiment_analysis = get_old_sentiment(reviewId, model)
        if sentiment_analysis:
            response_object["message"] = "El sentimiento ya existe."
            return response_object, 400
        
        sent = add_sentiment(reviewId=reviewId, stars=stars, 
                      sentiment=sentiment, anger=anger, item=item,
                      brand=brand, language=language, source=source, model=model, 
                      correct=correct, processTime=processTime, tokens=tokens
                      )
        response_object["message"] = f"Se ha añadido el sentimento para la reseña {reviewId}."
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
        "datasetId": fields.Integer,
        "id": fields.Integer,
        "stars": fields.Integer,
        "sentiment": fields.String,
        "originalStars": fields.Integer,
        "reviewText": fields.String,
        "model": fields.String,
        "processTime": fields.Integer,
        "tokens": fields.Integer,
        "productId": fields.String,
    },
)
#
class SentimentListByUser(Resource):
    @sentiments_namespace.marshal_with(sentiments_review, as_list=True)
    @sentiments_namespace.expect(parser)
    def get(self, review_user_id):
        """Devuelve todos los sentimientos de las reseñas."""
        check_token(request, sentiments_namespace)
        return get_sentiments_by_reviewuser_id(review_user_id=review_user_id), 200
    
class SentimentListByProduct(Resource):
    @sentiments_namespace.marshal_with(sentiments, as_list=True)
    @sentiments_namespace.expect(parser)
    def get(self, product_id):
        """Devuelve todos los sentimientos de las reseñas."""
        check_token(request, sentiments_namespace)
        return get_sentiments_by_product_id(product_id=product_id), 200

sentiments_namespace.add_resource(SentimentList, "")
sentiments_namespace.add_resource(SentimentListByUser, "/by_user/<string:review_user_id>")
sentiments_namespace.add_resource(SentimentListByProduct, "/by_product/<string:product_id>")
sentiments_namespace.add_resource(Sentiments, "/<int:sentiment_id>")