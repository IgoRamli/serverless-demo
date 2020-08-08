# Copyright 2018 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
This module is the Flask blueprint for the Product Catalog Service.
"""


import json
import time

from flask import Blueprint, render_template, jsonify, request
from flask.wrappers import Response

from helpers import product_catalog

product_catalog_page = Blueprint('product_catalog_page', __name__)


@product_catalog_page.route('/products', methods=['GET'])
def get_all_products():
    """
    Get the list of all products in Serverless Store
    """

    products = product_catalog.list_products()
    product_list = []
    for product in products:
        tmp = {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'created_at': product.created_at,
            'labels': product.labels,
            'image': product.image,
            'id': product.id
        }
        product_list.append(tmp)

    response = Response(
        response=json.dumps(product_list),
        status=200,
        mimetype='application/json'
    )
    return response


@product_catalog_page.route('/products/<product_id>', methods=['GET'])
def get_product_details(product_id):
    """
    Get the product details
    """

    try:
        products = product_catalog.get_product(product_id)
        return jsonify(products), 200
    except:
        return Response(status=404)


@product_catalog_page.route('/products', methods=['POST'])
def add_product():
    """
    Add new product
    """

    if request.method == 'POST' and request.is_json:
        try:
            req = request.get_json()
            product = product_catalog.Product(
                name=req['name'],
                description=req['description'],
                image=req['image'],
                labels=req['labels'],
                price=req['price'],
                created_at=int(time.time())
            )
            product_id = product_catalog.add_product(product)
            msg = {
                'result': 'Product added successfully!',
                'product_id': product_id
            }
            response = Response(
                response=json.dumps(msg),
                status=201,
                mimetype='application/json'
            )
            return response
        except:
            msg = {
                'error': 'Sorry! We were not able to add your product'
            }
            response = Response(
                response=json.dumps(msg),
                status=400,
                mimetype='application/json'
            )
            return response