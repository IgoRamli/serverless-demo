# Copyright 2020 Google LLC.
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
Cart Blueprint tests
"""


import os
import mock
import json
from unittest.mock import MagicMock, patch

import pytest

TEST_UID = 'TEST_UID'


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
    client = main.app.test_client()
    client.set_cookie('localhost', 'firebase_id_token', '*')
    return client

def test_cartGet_shouldReturn200(client):
    r = client.get('/cart')
    assert r.status_code == 200
    assert 'Shopping Cart' in str(r.data)

def test_cartPost_noId_shouldReturn400(client):
    r = client.post('/cart')
    assert r.status_code == 400

def test_cartPost_withId_shouldReturn200(client):
    import helpers
    from helpers import carts

    with patch.object(carts, 'add_to_cart', return_value=None) as add_to_cart:
        MOCK_ID = 1
        data = {
            'id': MOCK_ID
        }
        r = client.post('/cart', data=data)

    assert r.status_code == 200
    add_to_cart.assert_called_once()

def test_cartDelete_noId_shouldReturn400(client):
    r = client.delete('/cart')
    
    assert r.status_code == 400

def test_cartDelete_withId_shouldReturn200(client):
    MOCK_ID = 1
    data = {
        'id': MOCK_ID
    }
    r = client.delete(f'/cart', data=data)

    assert r.status_code == 200