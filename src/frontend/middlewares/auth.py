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
This module includes decorators for authenticating requests.
"""


from functools import wraps
from flask import redirect, request, url_for, make_response

from firebase_admin import auth
from firebase_admin.auth import ExpiredIdTokenError

FIREBASE_ID_TOKEN = 'firebase_id_token'


def loginAsAnonymous():
    response = make_response(redirect(url_for('product_catalog_page.display')))
    response.set_cookie(FIREBASE_ID_TOKEN, value='')
    return response


def verify_firebase_id_token(token):
    """
    A helper function for verifying ID tokens issued by Firebase.
    See https://firebase.google.com/docs/auth/admin/verify-id-tokens for
    more information.

    Parameters:
       token (str): A token issued by Firebase.

    Output:
       auth_context (dict): Authentication context.
    """
    try:
        full_auth_context = auth.verify_id_token(token)
    except ValueError:
        return {}
    except ExpiredIdTokenError:
        return {}

    auth_context = {
        'username': full_auth_context.get('name'),
        'uid': full_auth_context.get('uid'),
        'email': full_auth_context.get('email'),
        'expired': False
    }
    return auth_context


def auth_required(f):
    """
    A decorator for view functions that require authentication.
    If signed in, pass the request to the decorated view function with
    authentication context; otherwise redirect the request.

    Parameters:
       f (func): The view function to decorate.

    Output:
       decorated (func): The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        firebase_id_token = request.cookies.get(FIREBASE_ID_TOKEN)
        if not firebase_id_token:
            return loginAsAnonymous()

        auth_context = verify_firebase_id_token(firebase_id_token)
        if not auth_context:
            return loginAsAnonymous()

        return f(auth_context=auth_context, *args, **kwargs)
    return decorated

def auth_optional(f):
    """
    A decorator for view functions where authentication is optional.
    If signed in, pass the request to the decorated view function with
    authentication context.

    Parameters:
       f (func): The view function to decorate.

    Output:
       decorated (func): The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        firebase_id_token = request.cookies.get('firebase_id_token')
        if not firebase_id_token:
            return f(auth_context=None, *args, **kwargs)

        auth_context = verify_firebase_id_token(firebase_id_token)
        if not auth_context:
            return f(auth_context=None, *args, **kwargs)

        return f(auth_context=auth_context, *args, **kwargs)
    return decorated
