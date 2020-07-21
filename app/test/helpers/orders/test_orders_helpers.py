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

import os
import mock
from dataclasses import asdict
from unittest.mock import Mock, patch

import pytest

from google.cloud import firestore
import google.auth.credentials

import helpers
from helpers.orders import helpers, data_classes

"""
Cart Helper Functions Tests

Before running tests on this module, make sure that:
  - Firestore Emulator is running on http://localhost:8080
    To run Firestore Emulator, run this command in another terminal instance:
    `firebase emulators:start`
"""

MOCK_ORDER_1_ID = 'ORD1'
MOCK_ORDER_2_ID = 'ORD2'

MOCK_SHIPPING_1 = data_classes.Shipping(
    address_1='Pacific Century Place Tower Level 45 SCBD Lot 10',
    address_2='Jl. Jend. Sudirman No.53, RT.5/RW.3, Senayan, Kec. Kby. Baru',
    city='Jakarta Selatan',
    state='DKI Jakarta',
    zip_code='12190',
    email='google@google.com',
    mobile='(021) 30422800'
)
MOCK_SHIPPING_2 = data_classes.Shipping(
    address_1='Fakultas Ilmu Komputer Universitas Indonesia',
    address_2=None,
    city='Depok',
    state='Jawa Barat',
    zip_code='16424',
    email='cs@ui.ac.id',
    mobile='(081) 1234567890'
)

MOCK_PRODUCT_IDS_1 = ['1', '2', '3']
MOCK_PRODUCT_IDS_2 = ['1', '2']

MOCK_ORDER_1 = data_classes.Order(
    amount=30000,
    shipping=MOCK_SHIPPING_1,
    status='order_created',
    items=MOCK_PRODUCT_IDS_1,
    id=MOCK_ORDER_1_ID
)
MOCK_ORDER_2 = data_classes.Order(
    amount=20000,
    shipping=MOCK_SHIPPING_2,
    status='order_delivered',
    items=MOCK_PRODUCT_IDS_2
)

@pytest.fixture
def client():
    import main
    main.app.testing = True
    client = main.app.test_client()
    client.set_cookie('localhost', 'firebase_id_token', '*')

    # Connect to Firestore Emulator
    os.environ["FIRESTORE_DATASET"] = "test"
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8080/firestore"
    os.environ["FIRESTORE_HOST"] = "http://localhost:8080"
    os.environ["FIRESTORE_PROJECT_ID"] = "test"

    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    firestore_client = firestore.Client(project="test", credentials=credentials)
    tear_down_firestore(firestore_client)
    set_up_firestore(firestore_client)

    return client


def tear_down_firestore(firestore_client):
    collection = firestore_client.collection('orders')
    docs = collection.stream()
    for doc in docs:
        doc.reference.delete()


def set_up_firestore(firestore_client):
    collection = firestore_client.collection('orders')
    collection.document(MOCK_ORDER_1_ID).set(asdict(MOCK_ORDER_1))


def test_getOrder_shouldReturnOrder(client):
    res = helpers.get_order(MOCK_ORDER_1_ID)

    assert res == MOCK_ORDER_1


def test_addOrder_shouldAddOrderToFirestore(client):
    order_id = helpers.add_order(MOCK_ORDER_2)
    MOCK_ORDER_2.id = order_id

    res = helpers.get_order(order_id)

    assert res == MOCK_ORDER_2