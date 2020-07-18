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
System tests.
"""


import os
from unittest.mock import MagicMock
import pytest

TEST_UID = 'TEST_UID'
TEST_PRODUCT_ID = 'TEST_PRODUCT_ID'
TEST_PRODUCT_NAME = 'TEST_PRODUCT_NAME'

class Object(object):
    pass


@pytest.fixture
def client():
    """
    Gets a Flask Test Client with authentication disabled.
    """
    # Disable auth
    import middlewares.auth
    middlewares.auth.verify_firebase_id_token = MagicMock()
    middlewares.auth.verify_firebase_id_token.return_value = {
        'uid': TEST_UID,
        'username': 'user',
        'email': 'user@example.com'
    }

    # Mock cart
    from helpers import carts, product_catalog
    cart_obj = [Object()]
    setattr (cart_obj[0], 'item_id', TEST_PRODUCT_ID)
    carts.get_cart = MagicMock()
    carts.get_cart.return_value = cart_obj

    product_obj = Object()
    setattr (product_obj, 'name', TEST_PRODUCT_NAME)
    product_catalog.get_product = MagicMock()
    product_catalog.get_product.return_value = product_obj

    import main
    main.app.testing = True
    client = main.app.test_client()
    client.set_cookie('localhost', 'firebase_id_token', '*')
    return client


def test_product_catalog(client):
    """
    Should display the product catalog page.
    """
    r = client.get('/')
    assert r.status_code == 200
    assert 'Serverless Store' in str(r.data)


def test_cart(client):
    """
    Should display the cart page.
    """
    r = client.get('/cart')
    assert r.status_code == 200
    assert 'Shopping Cart' in str(r.data)


def test_checkout_single_product(client):
    """
    Should display the checkout page (single item).
    """
    r = client.get(f'/checkout?id={TEST_PRODUCT_ID}')
    assert r.status_code == 200
    assert f'{TEST_PRODUCT_NAME}' in str(r.data)


def test_checkout_cart(client):
    """
    Should redirect back to product display (cart).
    """
    r = client.get('/checkout?from_cart=1')
    assert r.status_code == 200
    assert f'{TEST_PRODUCT_NAME}' in str(r.data)


def test_sell(client):
    """
    Should display the sell page.
    """
    r = client.get('/sell')
    assert r.status_code == 200
    assert 'Join the marketplace' in str(r.data)


def test_signin(client):
    """
    Should display the sell page.
    """
    r = client.get('/signin')
    assert r.status_code == 200
