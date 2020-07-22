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
Charge Blueprint Tests
"""

import os
import requests
from unittest.mock import MagicMock, patch

import pytest

TEST_UID = 'TEST_UID'

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

def test_chargePost_noCheckoutForm_shouldReturn400(client):
    r = client.post('/charge')

    assert r.status_code == 400

def test_chargePost_withCheckoutFormValidation_shouldReturn400(client):
    import helpers
    from helpers import eventing, product_catalog
    product_catalog.calculate_total_price = MagicMock(return_value=0)

    data = {
        'product_ids-1': '1',
        'address_1': 'Address 1',
        'city': 'Jakarta Timur',
        'state': 'DKI Jakarta',
        'zip_code': '12345',
        'email': 'example@gmail.com',
        'mobile': '+62 8123456',
        'stripeToken': '1234567890'
    }
    with patch.object(eventing, 'stream_event', return_value=None) as stream_event:
        r = client.post('/charge', data=data)

    assert r.status_code == 200
    assert 'We are processing your order now' in str(r.data)
    stream_event.assert_called_once()