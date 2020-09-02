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
This module is the Flask blueprint for the charge page (/charge).
"""


import os
import logging
import requests

from flask import Blueprint, render_template, request, redirect, url_for
from opencensus.trace.tracer import Tracer
from opencensus.trace.exporters import stackdriver_exporter

from helpers import product_catalog
from middlewares.auth import auth_optional
from middlewares.form_validation import checkout_form_validation_required

BACKEND_URL = os.environ.get("BACKEND_URL", "backend.default.svc.cluster.default")

sde = stackdriver_exporter.StackdriverExporter()

charge_page = Blueprint('charge_page', __name__)

def generate_request_body(form):
    body = {
        'address_1': form.address_1.data,
        'address_2': form.address_2.data,
        'city': form.city.data,
        'state': form.state.data,
        'zip_code': form.zip_code.data,
        'email': form.email.data,
        'mobile': form.mobile.data,
        'stripeToken': form.stripeToken.data,
    }

    if (form.checkout_type.data == 'product'):
        body.update({ 'id': form.product_id.data })

    return body


@charge_page.route('/charge', methods=['POST'])
@auth_optional
@checkout_form_validation_required
def process(auth_context, form):
    """
    Call checkout function on back end service
    """

    checkout_type = form.checkout_type.data
    if checkout_type == 'product':
        url = f"{BACKEND_URL}/checkout/product"
    elif checkout_type == 'cart':
        url = f"{BACKEND_URL}/checkout/{auth_context['uid']}/cart"
    else:
        return redirect(url_for('product_catalog_page.display'))

    body = generate_request_body(form)
    logging.info(f"Calling backend with body {body}")
    requests.post(url, json=body)
    return render_template("charge.html", auth_context=auth_context)
    