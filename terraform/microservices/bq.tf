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