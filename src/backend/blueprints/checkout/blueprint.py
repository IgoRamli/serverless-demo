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
This module is the Flask blueprint for the checkout page (/checkout).
"""


import logging
import os

from flask import Blueprint, render_template, request
from flask_cors import CORS
from opencensus.trace.tracer import Tracer
from opencensus.trace.exporters import stackdriver_exporter

from helpers import eventing, orders, product_catalog, carts

PUBSUB_TOPIC_PAYMENT_PROCESS = os.environ.get('PUBSUB_TOPIC_PAYMENT_PROCESS')

sde = stackdriver_exporter.StackdriverExporter()

checkout_page = Blueprint("checkout_page", __name__)
CORS(checkout_page)

def get_product_ids_from_cart(uid):
    product_ids = []
    cart = carts.get_cart(uid)
    for item in cart:
        product = item.item_id
        product_ids.append(product)
    return product_ids


def get_shipping_address(args):
    shipping = orders.Shipping(address_1=args['address_1'],
                                address_2=args['address_2'],
                                city=args['city'],
                                state=args['state'],
                                zip_code=args['zip_code'],
                                email=args['email'],
                                mobile=args['mobile'])
    return shipping


def create_order(product_ids, stripe_token, shipping):
    # Create an OpenCensus tracer to trace each payment process, and export
    # the data to Stackdriver Tracing.
    tracer = Tracer(exporter=sde)
    trace_id = tracer.span_context.trace_id

    # Prepare the order
    with tracer.span(name="prepare_order_info"):
        amount = product_catalog.calculate_total_price(product_ids)
        order = orders.Order(amount=amount,
                             shipping=shipping,
                             status="order_created",
                             items=product_ids)
        order_id = orders.add_order(order)

    # Stream a Payment event
    with tracer.span(name="send_payment_event"):
        if stripe_token:
            # Publish an event to the topic for new payments.
            # Cloud Function pay_with_stripe subscribes to the topic and
            # processes the payment using the Stripe API upon arrival of new
            # events.
            # Cloud Function streamEvents (or App Engine service stream-event)
            # subscribes to the topic and saves the event to BigQuery for
            # data analytics upon arrival of new events.
            eventing.stream_event(
                topic_name=PUBSUB_TOPIC_PAYMENT_PROCESS,
                event_type='order_created',
                event_context={
                    'order_id': order_id,
                    'token': stripe_token,
                    # Pass the trace ID in the event so that Cloud Function
                    # pay_with_stripe can continue the trace.
                    'trace_id': trace_id,
                    'email': shipping.email
                }
            )


@checkout_page.route('/checkout/<uid>/cart', methods=['POST'])
def checkout_cart(uid):
    if request.method == 'POST' and request.is_json:
        json = request.get_json()
        shipping = get_shipping_address(json)
        product_ids = get_product_ids_from_cart(uid)
        stripe_token = json['stripeToken']

        logging.info(f"Checking out by cart with uid ({uid}) {json}")
        create_order(product_ids, stripe_token, shipping)

        return "Order successfully created!", 201


@checkout_page.route('/checkout/product', methods=['POST'])
def checkout_product():
    if request.method == 'POST' and request.is_json:
        json = request.get_json()
        shipping = get_shipping_address(json)
        product_ids = [ json['id'] ]
        stripe_token = json['stripeToken']

        logging.info(f"Checking out by product {json}")
        create_order(product_ids, stripe_token, shipping)

        return "Order successfully created!", 201