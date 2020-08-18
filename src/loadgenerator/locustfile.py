import os
import json
import random
import firebase_admin

from bs4 import BeautifulSoup
from locust import HttpUser, task, between
from firebase_admin import auth

INF = pow(10, 10)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend.backend.svc.cluster.local")
FRONTEND_URL = os.environ.get("FRONTEND_ADDR", "http://frontend.frontend.svc.cluster.local")

USER_LIST = []

rev_id = 8

# Initialize Firebase Admin SDK.
# See https://firebase.google.com/docs/admin/setup for more information.
firebase_admin.initialize_app()

class WebsiteUser(HttpUser):

    wait_time = between(1, 10)

    uid = None
    token = None

    def on_start(self):
        self.index()


    def get_product_list(self):
        response = self.client.get(f"{BACKEND_URL}/products")
        return response.json()


    def create_new_user(self):
        user_id = len(USER_LIST) + 1
        user = auth.create_user(
            email=f'user{rev_id}-{user_id}@serverlessstore.com',
            email_verified=False,
            password='locustUser',
            display_name=f'User {user_id} Rev. {rev_id}',
            disabled=False
        )
        USER_LIST.append(user.uid)


    def choose_user(self):
        idx = random.randint(0, len(USER_LIST))
        if (idx == len(USER_LIST)):
            self.create_new_user()
        return auth.get_user(USER_LIST[idx])


    @task(1)
    def login(self):
        user = self.choose_user()

        # Simulate a login call
        self.client.get(f"{FRONTEND_URL}/signin")
        self.uid = user.uid
        # Generate JWT Token
        token = auth.create_custom_token(user.uid)
        self.token = token
        # After signing in, user will always be redirected to main page
        self.client.get(f"{FRONTEND_URL}")
        return token


    @task(1)
    def index(self):
        self.client.get("/")

    
    @task(1)
    def get_cart(self, logged_in=False):
        if not logged_in:
            self.login()
        self.client.get(f"{BACKEND_URL}/carts/{self.uid}")


    @task(2)
    def add_to_cart(self):
        self.login()

        product_id = random.choice(self.get_product_list()).get('id')
        self.client.post(
            f"{FRONTEND_URL}/api/carts/{self.uid}",
            json={ 'item_id': product_id }
        )


    @task(2)
    def remove_from_cart(self):
        self.login()

        cart = self.client.get(f"{BACKEND_URL}/carts/{self.uid}").json()
        if len(cart) == 0:
            # Add an item first
            self.index()
            product_id = random.choice(self.get_product_list()).get('id')
            self.client.post(
                f"{FRONTEND_URL}/api/carts/{self.uid}",
                json={ 'item_id': product_id }
            )
        self.get_cart(logged_in=True)  # Go to cart page first
        cart = self.client.get(f"{BACKEND_URL}/carts/{self.uid}").json()
        product_id = random.choice(cart).get('item_id')
        self.client.delete(f"{FRONTEND_URL}/api/carts/{self.uid}/{product_id}")


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
            'stripeToken': 'tok_visa',
            'csrf_token': csrf_token,
            'checkout_type': 'product'
        })

    @task(1)
    def purchase_cart(self):
        self.client.post(f"{BACKEND_URL}/checkout/{self.uid}/cart", json={
            'address_1': '1600 Amphitheatre Parkway',
            'address_2': '1600 Amphitheatre Parkway',
            'zip_code': '94043',
            'city': 'Mountain View',
            'state': 'CA',
            'email': 'inigor.serverlessstore@gmail.com',
            'mobile': '1234567890',
            'stripeToken': 'tok_visa',
            }
        )
