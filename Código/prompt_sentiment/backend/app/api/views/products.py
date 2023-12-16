import logging
from flask import request
from flask_restx import Resource, fields, Namespace
from app.api.services.tokens import check_token
from app.api.services.roles import user_has_rol
from app.api.services.products import (
    get_all_products,
    get_product_by_id,
    get_products_with_sentiments,
    add_product,
    update_product,
    delete_product    
)

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

# Products
products_namespace = Namespace("products")

products = products_namespace.model(
    "Product",
    {
        "productId": fields.String(readOnly=True),
        "title": fields.String,
    },
)
put_parser = products_namespace.parser()
put_parser.add_argument("Authorization", location="headers")
put_parser.add_argument("productId", location="json")
put_parser.add_argument("title", location="json")

parser = products_namespace.parser()
parser.add_argument("Authorization", location="headers")

class ProductList(Resource):
    @products_namespace.marshal_with(products, as_list=True)
    @products_namespace.expect(parser)
    def get(self):
        """Devuelve todos los productos."""
        check_token(request, products_namespace)
        return get_all_products(), 200
    
    @products_namespace.marshal_with(products)
    @products_namespace.response(201, "El producto <productId> se ha agregado.")
    @products_namespace.response(400, "El producto ya existe.")
    @products_namespace.expect(put_parser)
    def post(self):
        """Crea un producto."""
        if not user_has_rol(request, "Admin", products_namespace):
            products_namespace.abort(403, "El usuario no es administrador.")
        post_data = request.get_json()
        productId = post_data.get("productId")
        title = post_data.get("title")
        response_object = {}
        reviewuser = get_product_by_id(productId=productId)
        if reviewuser:
            response_object["message"] = "El producto ya existe."
            return response_object, 400
        add_product(productId=productId, title = title)
        response_object["message"] = f"Se ha añadido el producto: {title}."
        return response_object, 201

class Products(Resource):
    @products_namespace.marshal_with(products)
    @products_namespace.response(200, "Correcto")
    @products_namespace.response(404, "El producto <productId> no existe.")
    @products_namespace.expect(parser)
    def get(self, productId):
        """Devuelve un producto."""
        check_token(request, products_namespace)
        product = get_product_by_id(productId)
        if not product:
            products_namespace.abort(404, f"El producto {productId} no existe.")
        return product, 200

    @products_namespace.expect(put_parser, validate=True)
    @products_namespace.response(200, "Producto <product_asin> actualizado.")
    @products_namespace.response(404, "El producto <product_asin> no existe.")
    def put(self, productId):
        """Actualiza un producto."""
        if not user_has_rol(request, "Admin", products_namespace):
            products_namespace.abort(403, "El usuario no es administrador.")
        post_data = request.get_json()
        title = post_data.get("title")
        response_object = {}
        product = get_product_by_id(productId)
        if not product:
            products_namespace.abort(404, f"El producto {productId} no existe.")
        update_product(product, title)
        response_object["message"] = f"Usuario {product.productId} actualizado."
        return response_object, 200

    @products_namespace.response(200, "Producto <productId> eliminado.")
    @products_namespace.response(404, "El producto <productId> no existe.")
    @products_namespace.expect(parser)
    def delete(self, productId):
        """Borra un producto."""
        if not user_has_rol(request, "Admin", products_namespace):
            products_namespace.abort(403, "El usuario no es administrador.")
        response_object = {}
        product = get_product_by_id(productId)
        if not product:
            products_namespace.abort(404, f"El producto {productId} no existe.")
        delete_product(product)
        response_object["message"] = f"El product {product.productId} se ha borrado."
        return response_object, 200
    
class ProductsSentiment(Resource):
    @products_namespace.marshal_with(products, as_list=True)
    @products_namespace.expect(parser)
    def get(self, dataset_id):
        """Devuelve todos los products de las reseñas."""
        check_token(request, products_namespace)
        return get_products_with_sentiments(dataset_id), 200

products_namespace.add_resource(ProductList, "")
products_namespace.add_resource(ProductsSentiment,"/sentiment/<int:dataset_id>")
products_namespace.add_resource(Products, "/<int:productId>")
