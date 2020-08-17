import os
import json
import random

from bs4 import BeautifulSoup
from locust import HttpUser, task, between

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend.backend.svc.cluster.local")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://frontend.frontend.svc.cluster.local")

class WebsiteUser(HttpUser):

    wait_time = between(1, 10)

    def on_start(self):
        self.index()

    def get_product_list(self):
        response = self.client.get(f"{BACKEND_URL}/products")
        return response.json()

    @task(1)
    def index(self):
        self.client.get("/")

    @task(1)
    def checkout_with_product(self):
        # Choose a product
        product_list = self.get_product_list()
        product_id = random.choice(product_list).get('id')

        # Checkout with that product
        self.client.get(f"{FRONTEND_URL}/checkout?id={product_id}")

    @task(1)
    def purchase_product(self):
        product_id = random.choice(self.get_product_list()).get('id')

        response = self.client.get(f"{FRONTEND_URL}/checkout?id={product_id}")
        html_text = response.text
        csrf_token = BeautifulSoup(html_text, 'html.parser').find(id='csrf_token')["value"]

        self.client.post(f"{FRONTEND_URL}/charge", {
            'product_id': product_id,
            'address_1': '1600 Amphitheatre Parkway',
            'address_2': '1600 Amphitheatre Parkway',
            'zip_code': '94043',
            'city': 'Mountain View',
            'state': 'CA',
            'email': 'inigor.serverlessstore@gmail.com',
            'mobile': '1234567890',
            'stripeToken': 'abcde',
            'csrf_token': csrf_token,
            'checkout_type': 'product'
        })