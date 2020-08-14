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


# This module includes decorators for validating forms.
# The module uses library Flask-WTF for form validation. See
# https://flask-wtf.readthedocs.io/en/stable/ for more information.


from functools import wraps

from flask import request
from flask_wtf import FlaskForm
from wtforms import FieldList, FloatField, StringField
from wtforms.validators import DataRequired, Optional


class SellForm(FlaskForm):
    """
    FlaskForm for selling items.
    """
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])
    image = StringField('image', validators=[DataRequired()])


class CheckOutForm(FlaskForm):
    """
    FlaskForm for checking out items.
    """
    product_id = StringField('product_id', validators=[Optional()])
    address_1 = StringField('address_1', validators=[DataRequired(message='addr_1')])
    address_2 = StringField('address_2', validators=[Optional()])
    city = StringField('city', validators=[DataRequired(message='city')])
    state = StringField('state', validators=[DataRequired(message='state')])
    zip_code = StringField('zip_code', validators=[DataRequired(message='zip_code')])
    email = StringField('email', validators=[DataRequired(message='email')])
    mobile = StringField('mobile', validators=[DataRequired(message='mobile')])
    stripeToken = StringField('stripeToken', validators=[DataRequired(message='stripeToken')])
    checkout_type = StringField('checkout_type', validators=[DataRequired(message='checkout_type')])


def sell_form_validation_required(f):
    """
    A decorator for validating requests with the sell form.
    Returns an error message if validation fails.

    Parameters:
       f (func): The view function to decorate.

    Output:
       decorated (func): The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        sell_form = SellForm()
        if not sell_form.validate():
            return 'Something does not look right. Check your input and try again.', 400

        return f(form=sell_form, *args, **kwargs)
    return decorated


def checkout_form_validation_required(f):
    """
    A decorator for validating requests with the check out form.
    Returns an error message if validation fails.

    Parameters:
       f (func): The view function to decorate.

    Output:
       decorated (func): The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        checkout_form = CheckOutForm(request.form)
        if not checkout_form.validate():
            return 'Something does not look right. Check your input and try again.', 400

        return f(form=checkout_form, *args, **kwargs)
    return decorated
