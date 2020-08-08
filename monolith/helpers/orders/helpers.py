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
A collection of helper functions for order related operations.
"""


import os
from dataclasses import asdict
import uuid

from google.cloud import firestore
import google.auth.credentials

from .data_classes import Order

PROJECT = os.environ.get('GCP_PROJECT')

firestore_client = firestore.Client(project=PROJECT)

if not os.getenv('GAE_ENV', '').startswith('standard'):
    # Connect to Firestore Emulator
    import mock
    print('Connecting to Firestore Emulator...')
    os.environ["FIRESTORE_DATASET"] = "test"
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8080/firestore"
    os.environ["FIRESTORE_HOST"] = "http://localhost:8080"
    os.environ["FIRESTORE_PROJECT_ID"] = "test"

    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    firestore_client = firestore.Client(project="test", credentials=credentials)


def add_order(order):
    """
    Helper function for adding an order.

    Parameters:
       order (Order): An Order object.

    Output:
       The ID of the order.
    """
    order_id = uuid.uuid4().hex
    firestore_client.collection('orders').document(order_id).set(asdict(order))
    return order_id


def get_order(order_id):
    """
    Helper function for getting an order.

    Parameters:
       order_id (str): The ID of the order.

    Output:
       An Order object.
    """
    order_data = firestore_client.collection('orders').document(order_id).get()
    return Order.deserialize(order_data)
