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
A collection of helper functions for cart related operations.
"""


import os
import requests
import json

from dataclasses import asdict
import time
import mock
from flask import current_app

from google.cloud import firestore
import google.auth.credentials

from .data_classes import CartItem

PROJECT = os.environ.get('GCP_PROJECT')

firestore_client = firestore.Client(project=PROJECT)

BACKEND_URL = os.environ.get("BACKEND_URL", "backend.default.svc.cluster.default")


def get_cart(uid):
    """
    Helper function for getting all items in a cart.

    Parameters:
       uid (str): The unique ID of an user.

    Output:
       A list of CartItem.
    """

    url = f"{BACKEND_URL}/carts/{uid}"
    
    result = requests.get(url).text
    cart = json.loads(result)

    return [ CartItem.deserialize(item) for item in cart ]


def add_to_cart(uid, item_id):
    """
    Helper function for adding an item to a cart.

    Parameters:
       uid (str): The unique ID of an user.
       item_id (str): The ID of an item.

    Output:
       None.
    """

    url = f"{BACKEND_URL}/carts/{uid}"
    body = {
        'item_id': item_id,
    }

    requests.post(url, json=body)


def remove_from_cart(uid, item_id):
    """
    Helper function for deleting an item from a cart.

    Parameters:
       uid (str): The unique ID of an user.
       item_id (str): The ID of an item.

    Output:
       None.
    """

    url = f"{BACKEND_URL}/carts/{uid}/{item_id}"

    requests.delete(url)
