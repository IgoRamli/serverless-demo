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
A collection of helper functions for streaming events.
"""


import os
import logging
import json
import time

from google.cloud import pubsub_v1
import google.auth.credentials

publisher = pubsub_v1.PublisherClient()

if not os.getenv('GAE_ENV', '').startswith('standard'):
    # Connect to Firestore Emulator
    import mock
    print('Connecting to Pub/Sub Emulator...')
    os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
    os.environ["PUBSUB_PROJECT_ID"] = "test"
    os.environ["GCP_PROJECT"] = "test"

    credentials = mock.Mock(spec=google.auth.credentials.Credentials)
    publisher = pubsub_v1.PublisherClient(credentials=credentials)

GCP_PROJECT = os.environ.get('GCP_PROJECT')


def stream_event(topic_name, event_type, event_context):
    """
    Helper function for publishing an event.

    Parameters:
       topic_name (str): The name of the Cloud Pub/Sub topic.
       event_type (str): The type of the event.
       event_context: The context of the event.

    Output:
       None.
    """

    topic_path = publisher.topic_path(GCP_PROJECT, topic_name)
    request = {
        'event_type': event_type,
        'created_time': str(int(time.time())),
        'event_context': event_context
    }
    data = json.dumps(request).encode()
    logging.info(f"Publishing {data} on topic {topic_path}")
    publisher.publish(topic_path, data)