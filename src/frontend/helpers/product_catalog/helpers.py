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
import json
import os
import requests
import uuid

from google.cloud import firestore
import google.auth.credentials

from .data_classes import Product, PromoEntry

PROJECT = os.environ.get('GCP_PROJECT')

BUCKET = os.environ.get('GCS_BUCKET')

firestore_client = firestore.Client(project=PROJECT)

BACKEND_URL = os.environ.get("BACKEND_URL", "backend.default.svc.cluster.default")


def add_product(product):
    """
    Helper function for adding a product.

    Parameters:
        product (Product): A Product object.

    Output:
        The ID of the product.
    """

    url = f"{BACKEND_URL}/products"
    product_dict = {
        'name': product.name,
        'description': product.description,
        'image': product.image,
        'labels': product.labels,
        'price': product.price
    }

    result = requests.post(url, json=product_dict).text

    product_id = json.loads(result)['product_id']
    
    return product_id


def get_product(product_id):
    """
    Helper function for getting a product.

    Parameters:
       product_id (str): The ID of the product.

    Output:
       A Product object.
    """

    url = f"{BACKEND_URL}/products/{product_id}"

    result = requests.get(url).text

    product = json.loads(result)

    return Product.deserialize(product)


def list_products():
    """
    Helper function for listing products.

    Parameters:
       None.

    Output:
       A list of Product objects.
    """

    url = f"{BACKEND_URL}/products"

    result = requests.get(url).text

    products = json.loads(result)
    product_list = []
    for product in products:
        product_list.append(Product.deserialize(product))

    return product_list


def get_promos():
    """
    Helper function for getting promoted products.

    Parameters:
       None.

    Output:
       A list of Product objects.
    """

    url = f'{BACKEND_URL}/promos'

    result = requests.get(url).text

    products = json.loads(result)
    promos = [ Product.deserialize(item) for item in products ]

    return promos
