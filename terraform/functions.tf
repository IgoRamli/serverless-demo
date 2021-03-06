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

resource "google_cloudfunctions_function" "cf_automl" {
  project     = var.project
  region      = var.cfunction_region

  name        = var.cf_automl_name
  description = "Send product for processing by AutoML"
  runtime     = "python37"
  entry_point = "automl"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.storage_cfunctions.name
  source_archive_object = google_storage_bucket_object.cfunctions_src["automl"].name
  event_trigger {
      event_type = "google.pubsub.topic.publish"
      resource   = google_pubsub_topic.new_product.id
  }
  environment_variables = {
      AUTOML_MODEL_ID = var.automl_model_id
      GCS_BUCKET      = google_storage_bucket.product_image.name
  }
}

resource "google_cloudfunctions_function" "cf_detect_labels" {
  project     = var.project
  region      = var.cfunction_region

  name        = var.cf_detect_labels_name
  description = "Send product to Cloud Vision for label detection"
  runtime     = "python37"
  entry_point = "detect_labels"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.storage_cfunctions.name
  source_archive_object = google_storage_bucket_object.cfunctions_src["detect_labels"].name
  event_trigger {
      event_type = "google.pubsub.topic.publish"
      resource   = google_pubsub_topic.new_product.id
  }
  environment_variables = {
      GCS_BUCKET      = google_storage_bucket.product_image.name
  }
}

resource "google_cloudfunctions_function" "cf_pay_with_stripe" {
  project     = var.project
  region      = var.cfunction_region

  name        = var.cf_pay_with_stripe_name
  description = "Send payment request to Stripe"
  runtime     = "python37"
  entry_point = "pay_with_stripe"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.storage_cfunctions.name
  source_archive_object = google_storage_bucket_object.cfunctions_src["pay_with_stripe"].name
  event_trigger {
      event_type = "google.pubsub.topic.publish"
      resource   = google_pubsub_topic.payment_process.id
  }
  environment_variables = {
    STRIPE_API_KEY                  = var.stripe_api_key
    PUBSUB_TOPIC_PAYMENT_COMPLETION = google_pubsub_topic.payment_completion.name
  }
}

resource "google_cloudfunctions_function" "cf_streamEvents" {
  project     = var.project
  region      = var.cfunction_region

  name        = var.cf_streamEvents_name
  description = "Record events to BigQuery"
  runtime     = "nodejs10"
  entry_point = "streamEvents"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.storage_cfunctions.name
  source_archive_object = google_storage_bucket_object.cfunctions_src["streamEvents"].name
  trigger_http          = true

  environment_variables = {
      GCS_BUCKET      = google_storage_bucket.product_image.name
  }
}

resource "google_cloudfunctions_function" "cf_upload_image" {
  project     = var.project
  region      = var.cfunction_region

  name        = var.cf_upload_image_name
  description = "Upload image to Cloud Storage"
  runtime     = "python37"
  entry_point = "upload_image"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.storage_cfunctions.name
  source_archive_object = google_storage_bucket_object.cfunctions_src["upload_image"].name
  trigger_http          = true

  environment_variables = {
    BIGQUERY_DATASET = var.bq_dataset,
    BIGQUERY_TABLE   = var.bq_table
  }
}

resource "google_cloudfunctions_function_iam_member" "cf_upload_image_invoker" {
  project        = google_cloudfunctions_function.cf_upload_image.project
  region         = google_cloudfunctions_function.cf_upload_image.region
  cloud_function = google_cloudfunctions_function.cf_upload_image.name

  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${google_service_account.microservice_fr.email}"
}

# Enable cloud functions API