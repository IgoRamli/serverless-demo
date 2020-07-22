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
Checkout Blueprint Tests
"""

import os
from unittest.mock import MagicMock

import pytest

TEST_UID = os.environ.get('TEST_UID')
TEST_PRODUCT_ID = os.environ.get('TEST_PRODUCT_ID')
TEST_PRODUCT_NAME = os.environ.get('TEST_PRODUCT_NAME')

class Object():
    pass

@pytest.fixture
def client():
    """
    Gets a Flask Test Client with authentication disabled.
    """
    # Disable auth
    import middlewares
    from middlewares import auth
    middlewares.auth.verify_firebase_id_token = MagicMock()
    middlewares.auth.verify_firebase_id_token.return_value = {
        'uid': TEST_UID,
        'username': 'user',
        'email': 'user@example.com'
    }

    import main
    main.app.testing = True
    main.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF to ease testing
    client = main.app.test_client()
    client.set_cookie('localhost', 'firebase_id_token', '*')
    return client

def test_checkoutGet_withProductId_shouldReturn200(client):
    import helpers
    from helpers import product_catalog
    product_catalog.get_product = MagicMock()
    product_catalog.get_product.return_value = Object()
    setattr(product_catalog.get_product.return_value, 'name', TEST_PRODUCT_NAME)

    r = client.get('/checkout?id=1')

    assert r.status_code == 200

def test_checkoutGet_withCartId_shouldreturn200(client):
    import helpers
    from helpers import carts, product_catalog
    carts.get_cart = MagicMock()
    carts.get_cart.return_value = [Object()]
    setattr(carts.get_cart.return_value[0], 'item_id', TEST_PRODUCT_ID)

    product_catalog.get_product = MagicMock()
    product_catalog.get_product.return_value = Object()
    setattr(product_catalog.get_product.return_value, 'name', TEST_PRODUCT_NAME)

    r = client.get('/checkout?from_cart=1')

    assert r.status_code == 200

def test_checkoutGet_withoutParam_shouldRedirectToCatalogDisplay(client):
    r = client.get('/checkout', follow_redirects=False)

    assert r.status_code == 302
    assert '\"/\"' in str(r.data)