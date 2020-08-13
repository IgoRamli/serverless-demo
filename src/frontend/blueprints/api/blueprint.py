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
This module is the Flask blueprint for the cart page (/cart).
"""


import logging
import os
import requests
from flask import Blueprint, render_template, request

from helpers import carts, product_catalog
from middlewares.auth import auth_required


api_page = Blueprint('api_page', __name__, url_prefix='/api')

BACKEND_URL = os.environ.get("BACKEND_URL", "backend.default.svc.cluster.default")


@api_page.route('/carts/<uid>', methods=['POST'])
def add_to_cart(uid):
    """
    Pass the add to cart request to back end
    """
    
    url = f"{BACKEND_URL}/carts/{uid}"
    body = request.get_json()

    req_msg = {
        'type': 'POST',
        'url': url,
        'body': body
    }
    logging.info(f"Calling {req_msg} to add item from cart")

    result = requests.post(url=url, json=body)

    if(result.status_code != 200):
        return 'Adding product failed!', 400

    return 'Product added successfully!', 200


@api_page.route('/carts/<uid>/<id>', methods=['DELETE'])
def remove_from_cart(uid, id):
    """
    Pass the add to cart request to back end
    """
    
    url = f"{BACKEND_URL}/carts/{uid}/{id}"
    
    req_msg = {
        'type': 'DELETE',
        'url': url
    }
    logging.info(f"Calling {req_msg} to add item from cart")

    result = requests.delete(url)

    if(result.status_code != 200):
        return 'Deleting product failed!', 400

    return 'Product deleted successfully!', 200