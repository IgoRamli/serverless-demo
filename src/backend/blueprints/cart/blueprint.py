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


from flask import Blueprint, render_template, request, jsonify
from flask_cors import CORS

from helpers import carts


cart_page = Blueprint('cart_page', __name__)
CORS(cart_page)


@cart_page.route('/carts/<uid>', methods=['GET'])
def get_cart(uid):
    """
    Endpoint for getting cart items

    Args:
        uid (String): User ID

    Returns:
        JSON object describing user cart. Returns empty JSON if cart doesn't exist.
    """
    cart = carts.get_cart(uid)
    response = []
    for item in cart:
        response.append({
            'item_id': item.item_id,
            'document_id': item.document_id,
            'modify_time': item.modify_time,
            'uid': item.uid
        })
    return jsonify(response), 200


@cart_page.route('/carts/<uid>', methods=['POST'])
def add_cart_item(uid):
    """
    Endpoint for adding an item to cart.

    Parameters:
       auth_context (dict): The authentication context of request.
                            See middlewares/auth.py for more information.
    Output:
       Text message with HTTP status code 200.
    """

    if request.method == 'POST' and request.is_json:
        item_id = request.get_json()['item_id']
        if item_id:
            carts.add_to_cart(uid, item_id)
            return "Operation completed.", 200

    return "Operation Failed", 400


@cart_page.route('/carts/<uid>/<id>', methods=['DELETE'])
def remove_cart_item(uid, id):
    """
    Endpoint for removing an item from cart.

    Parameters:
       uid (String) : User ID who added items
       id (String)  : Product ID to be added
    Output:
       Text message with HTTP status code 200.
    """

    if id:
        carts.remove_from_cart(uid, id)
        return "Operation completed.", 200

    return "Operation Failed", 400
