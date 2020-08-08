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
import uuid
from dataclasses import asdict
from unittest.mock import Mock, patch

import pytest

from google.cloud import firestore
import google.auth.credentials

import helpers
from helpers.product_catalog import helpers, data_classes

"""
Cart Helper Functions Tests

Before running tests on this module, make sure that:
  - Firestore Emulator is running on http://localhost:8080
    To run Firestore Emulator, run this command in another terminal instance:
    `firebase emulators:start`
"""

MOCK_TIME_1 = 1578718800  # 11 January 2020 12:00:00 GMT+07:00
MOCK_TIME_2 = 1593406800  # 29 June 2020 12:00:00 GMT+07:00

MOCK_PRODUCT_1 = data_classes.Product(
    name='First Product',
    description='First Description',
    image='first_image.png',
    labels=[],
    price=10000,
    created_at=MOCK_TIME_1,
    id=uuid.uuid4().hex
)

MOCK_PRODUCT_2 = data_classes.Product(
    name='Second Product',
    description='Second Description',
    image='second_image.png',
    labels=[],
    price=15000,
    created_at=MOCK_TIME_2,
    id=uuid.uuid4().hex
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
    collection = firestore_client.collection('products')
    docs = collection.stream()
    for doc in docs:
        doc.reference.delete()

    collection = firestore_client.collection('promos')
    docs = collection.stream()
    for doc in docs:
        doc.reference.delete()


def set_up_firestore(firestore_client):
    collection = firestore_client.collection('products')
    collection.document(MOCK_PRODUCT_1.id).set(asdict(MOCK_PRODUCT_1))

    promos = firestore_client.collection('promos')
    promos.document(MOCK_PRODUCT_1.id).set({
        'label': 'pets',
        'score': 0.75
    })


def test_getProduct_shouldReturnProduct(client):
    res = helpers.get_product(MOCK_PRODUCT_1.id)

    assert res == MOCK_PRODUCT_1


def test_addProduct_shouldReturnProductId(client):
    product_id = helpers.add_product(MOCK_PRODUCT_2)
    MOCK_PRODUCT_2.id = product_id

    res = helpers.get_product(product_id)

    assert res == MOCK_PRODUCT_2

def test_listProducts_shouldReturnAllProducts(client):
    product_id = helpers.add_product(MOCK_PRODUCT_2)
    MOCK_PRODUCT_2.id = product_id

    res = helpers.list_products()

    assert res == [MOCK_PRODUCT_1, MOCK_PRODUCT_2]

def test_calculateTotalPrice_shouldReturnTotalPrice(client):
    product_id = helpers.add_product(MOCK_PRODUCT_2)
    MOCK_PRODUCT_2.id = product_id

    product_ids = [MOCK_PRODUCT_1.id, MOCK_PRODUCT_2.id]
    res = helpers.calculate_total_price(product_ids)

    assert res == 25000

def test_calculateTotalPrice_noProduct_shouldReturnZero(client):
    res = helpers.calculate_total_price([])

    assert res == 0

def test_getPromos_shouldReturnPetProducts():
    res = helpers.get_promos()
    print(res)

    assert res == [MOCK_PRODUCT_1]