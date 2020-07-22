# Copyright 2020 Google LLC.
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

import os
import mock
import uuid
from dataclasses import asdict
from unittest.mock import Mock, patch

import pytest

from google.cloud import pubsub_v1
import google.auth.credentials

import helpers
from helpers.eventing import helpers

"""
Cart Helper Functions Tests

Before running tests on this module, make sure that:
  - Firestore Emulator is running on http://localhost:8080
    To run Firestore Emulator, run this command in another terminal instance:
    `firebase emulators:start`
"""


@pytest.fixture
def client():
    import main
    main.app.testing = True
    client = main.app.test_client()
    client.set_cookie('localhost', 'firebase_id_token', '*')

    # Connect to Pub/Sub Emulator
    os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
    os.environ["PUBSUB_PROJECT_ID"] = "test"
    os.environ["GCP_PROJECT"] = "test"

    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    publisher = pubsub_v1.PublisherClient(credentials=credentials)
    tear_down_pubsub(publisher)
    set_up_pubsub(publisher)

    return client


def tear_down_pubsub(publisher):
    name = publisher.topic_path('test', 'sample_topic')
    publisher.delete_topic(name)


def set_up_pubsub(publisher):
    name = publisher.topic_path('test', 'sample_topic')
    publisher.create_topic(name)

def test_streamEvent_shouldPublishToPubSub(client):
    helpers.stream_event(
        topic_name='sample_topic',
        event_type='sample_event',
        event_context={
            'description': 'Sample Description'
        }
    )