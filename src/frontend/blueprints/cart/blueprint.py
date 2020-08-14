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


import os
from flask import Blueprint, render_template, request

from helpers import carts, product_catalog
from middlewares.auth import auth_required


cart_page = Blueprint('cart_page', __name__)

BACKEND_URL = os.environ.get("BACKEND_URL", "backend.default.svc.cluster.default")


@cart_page.route('/cart', methods=['GET'])
@auth_required
def display(auth_context):
    """
    View function for displaying the contents of the cart.

    Parameters:
        auth_context (dict): The authentication context of request.
                             See middlewares/auth.py for more information.
    Output:
        Rendered HTML page.
    """

    cart = carts.get_cart(auth_context.get('uid'))
    for item in cart:
        product = product_catalog.get_product(item.item_id)
        item.info = product

    return render_template("cart.html",
                           cart=cart,
                           auth_context=auth_context,
                           bucket=product_catalog.BUCKET,
                           backend_url=BACKEND_URL)