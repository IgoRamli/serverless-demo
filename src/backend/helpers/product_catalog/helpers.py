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
A collection of helper functions for product related operations.
"""


from dataclasses import asdict
import os
import logging
import uuid

from google.cloud import firestore
import google.auth.credentials

from .data_classes import Product, PromoEntry

PROJECT = os.environ.get('GCP_PROJECT')

BUCKET = os.environ.get('GCS_BUCKET')

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


def add_product(product):
    """
    Helper function for adding a product.

    Parameters:
       product (Product): A Product object.

    Output:
       The ID of the product.
    """

    product_id = uuid.uuid4().hex
    document = firestore_client.collection('products').document(product_id)
    document.set(asdict(product))
    return product_id


def get_product(product_id):
    """
    Helper function for getting a product.

    Parameters:
       product_id (str): The ID of the product.

    Output:
       A Product object.
    """

    collections = firestore_client.collection('products')
    product = collections.document(product_id).get()
    return Product.deserialize(product)


def list_products():
    """
    Helper function for listing products.

    Parameters:
       None.

    Output:
       A list of Product objects.
    """

    col = firestore_client.collection('products').order_by('created_at')
    products = col.get()
    product_list = [Product.deserialize(product) for product in list(products)]
    return product_list


def calculate_total_price(product_ids):
    """
    Helper function for calculating the total price of a list of products.

    Parameters:
       product_ids (List[str]): A list of product IDs.

    Output:
       The total price.
    """

    logging.info(f"Calculating total price of {product_ids}")
    total = 0
    for product_id in product_ids:
        product = get_product(product_id)
        total += int(product.price)
    return total


def get_promos():
    """
    Helper function for getting promoted products.

    Parameters:
       None.

    Output:
       A list of Product objects.
    """

    promos = []
    query = firestore_client.collection('promos')
    query = query.where('label', '==', 'pets').where('score', '>=', 0.7)
    query = query.order_by('score', direction=firestore.Query.DESCENDING)
    query = query.limit(3)
    query_results = query.get()
    for result in query_results:
        entry = PromoEntry.deserialize(result)
        product = get_product(entry.id)
        promos.append(product)
    return promos
