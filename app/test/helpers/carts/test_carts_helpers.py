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
from unittest.mock import Mock, patch

import pytest

from google.cloud import firestore
import google.auth.credentials

import helpers
from helpers.carts import helpers, data_classes

"""
Cart Helper Functions Tests

Before running tests on this module, make sure that:
  - Firestore Emulator is running on http://localhost:8080
    To run Firestore Emulator, run this command in another terminal instance:
    `firebase emulators:start`
"""

MOCK_UID = '1'
MOCK_UID_2 = '2'
MOCK_TIME_1 = 1578718800  # 11 January 2020 12:00:00 GMT+07:00
MOCK_TIME_2 = 1593406800  # 29 June 2020 12:00:00 GMT+07:00
MOCK_TIME_3 = 1578718860  # 11 January 2020 12:00:01 GMT+07:00
MOCK_ITEM_1_ID = 'ITM1'
MOCK_ITEM_2_ID = 'ITM2'
MOCK_ITEM_3_ID = 'ITM3'
MOCK_DOC_1_ID = 'DOC1'
MOCK_DOC_2_ID = 'DOC2'
MOCK_DOC_3_ID = 'DOC3'

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
    collection = firestore_client.collection('carts')
    docs = collection.stream()
    for doc in docs:
        doc.reference.delete()


def set_up_firestore(firestore_client):
    mock_item_1 = {
        'modify_time': MOCK_TIME_1,
        'uid': MOCK_UID,
        'item_id': MOCK_ITEM_1_ID,
        'document_id': MOCK_DOC_1_ID
    }
    mock_item_2 = {
        'modify_time': MOCK_TIME_2,
        'uid': MOCK_UID,
        'item_id': MOCK_ITEM_2_ID,
        'document_id': MOCK_DOC_2_ID
    }
    mock_item_3 = {
        'modify_time': MOCK_TIME_3,
        'uid': MOCK_UID_2,
        'item_id': MOCK_ITEM_3_ID,
        'document_id': MOCK_DOC_3_ID
    }
    collection = firestore_client.collection('carts')
    collection.document(MOCK_DOC_1_ID).set(mock_item_1)
    collection.document(MOCK_DOC_2_ID).set(mock_item_2)
    collection.document(MOCK_DOC_3_ID).set(mock_item_3)
    

def test_getCart_shouldReturnListOfCartItem(client):
    res = helpers.get_cart(MOCK_UID)

    expected = [
        data_classes.CartItem(
            document_id=MOCK_DOC_2_ID,
            item_id=MOCK_ITEM_2_ID,
            modify_time=MOCK_TIME_2,
            uid=MOCK_UID),
        data_classes.CartItem(
            document_id=MOCK_DOC_1_ID,
            item_id=MOCK_ITEM_1_ID,
            modify_time=MOCK_TIME_1,
            uid=MOCK_UID)
    ]
    assert res == expected

    res = helpers.get_cart(MOCK_UID_2)

    expected = [
        data_classes.CartItem(
            document_id=MOCK_DOC_3_ID,
            item_id=MOCK_ITEM_3_ID,
            modify_time=MOCK_TIME_3,
            uid=MOCK_UID_2),
    ]
    assert res == expected

def test_addToCart_shouldAddCartToFirebase(client):
    helpers.add_to_cart(MOCK_UID_2, MOCK_ITEM_1_ID)

    res = helpers.get_cart(MOCK_UID_2)

    assert len(res) == 2
    assert res[0].uid == MOCK_UID_2
    assert res[0].item_id == MOCK_ITEM_1_ID

def test_removeFromCart_shouldRemoveCartFromFirebase(client):
    helpers.remove_from_cart(MOCK_UID, MOCK_ITEM_1_ID)

    res = helpers.get_cart(MOCK_UID)

    assert res[0].uid == MOCK_UID
    assert res[0].item_id == MOCK_ITEM_2_ID