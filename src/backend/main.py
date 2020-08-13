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
This module is the main flask application.
"""


import firebase_admin
from flask import Flask
from flask_cors import CORS

from blueprints import cart_page, product_catalog_page, checkout_page, promo_page

import google.cloud.logging

# Instantiates a client
client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.get_default_handler()
client.setup_logging()

# Initialize Firebase Admin SDK.
# See https://firebase.google.com/docs/admin/setup for more information.
firebase = firebase_admin.initialize_app()


# Enable Google Cloud Debugger
# See https://cloud.google.com/debugger/docs/setup/python for more information.
try:
    import googleclouddebugger
    # googleclouddebugger.enable()
except ImportError:
    pass


app = Flask(__name__)
app.secret_key = b'A Super Secret Key'


app.register_blueprint(cart_page)
app.register_blueprint(checkout_page)
app.register_blueprint(product_catalog_page)
app.register_blueprint(promo_page)

CORS(app)


if __name__ == '__main__':
    app.run(debug=True)