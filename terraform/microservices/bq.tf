/**
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

resource "google_bigquery_dataset" "sample_data" {
  dataset_id                  = "sample_data"
  friendly_name               = "sample_data"
  description                 = "Dataset that contains user events and it's analytical DBs"
  location                    = "asia-east1"
}

resource "google_bigquery_table" "sample_table" {
  dataset_id = google_bigquery_dataset.sample_data.dataset_id
  table_id   = "sample_table"

  schema = <<EOF
[
  {
    "name": "eventType",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Type of event"
  },
  {
    "name": "createdTime",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "Miliseconds since epoch, describing the event creation time"
  },
  {
    "name": "context",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "JSON Object containing event context"
  }
]
EOF

}