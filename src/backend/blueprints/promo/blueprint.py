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

promo_page = Blueprint('promo_page', __name__)

@promo_page.route('/promos', methods=['GET'])
def get_promos():
    """
    Get list of recommended products
    """

    products = product_catalog.get_promos()
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

    return jsonify(product_list), "200"