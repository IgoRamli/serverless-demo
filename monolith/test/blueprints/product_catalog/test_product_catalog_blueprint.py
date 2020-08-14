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
Product Catalog Blueprint Tests
"""

import os
from unittest.mock import MagicMock

import pytest

TEST_UID = os.environ.get('TEST_UID')

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

def test_productCatalogGet_shouldReturn200(client):
    r = client.get('/')

    assert r.status_code == 200