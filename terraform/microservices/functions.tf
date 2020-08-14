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
  region      = var.region

  name        = "automl"
  description = "Send product for processing by AutoML"
  runtime     = "python37"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.storage_cfunctions.name
  source_archive_object = google_storage_bucket_object.cfunctions_src["automl"].name
  event_trigger {
      event_type = "google.pubsub.topic.publish"
      resource   = google_pubsub_topic.new_product.id
  }
}

resource "google_cloudfunctions_function" "cf_detect_labels" {
  project     = var.project
  region      = var.region

  name        = "detect_labels"
  description = "Send product to Cloud Vision for label detection"
  runtime     = "python37"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.storage_cfunctions.name
  source_archive_object = google_storage_bucket_object.cfunctions_src["detect_labels"].name
  event_trigger {
      event_type = "google.pubsub.topic.publish"
      resource   = google_pubsub_topic.new_product.id
  }
}

resource "google_cloudfunctions_function" "cf_pay_with_stripe" {
  project     = var.project
  region      = var.region

  name        = "pay_with_stripe"
  description = "Send payment request to Stripe"
  runtime     = "python37"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.storage_cfunctions.name
  source_archive_object = google_storage_bucket_object.cfunctions_src["pay_with_stripe"].name
  event_trigger {
      event_type = "google.pubsub.topic.publish"
      resource   = google_pubsub_topic.payment_process.id
  }
}

resource "google_cloudfunctions_function" "cf_upload_image" {
  project     = var.project
  region      = var.region

  name        = "upload_image"
  description = "Upload image to Cloud Storage"
  runtime     = "python37"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.storage_cfunctions.name
  source_archive_object = google_storage_bucket_object.cfunctions_src["upload_image"].name
  trigger_http          = true
}

resource "google_cloudfunctions_function_iam_member" "cf_upload_image_invoker" {
  project        = google_cloudfunctions_function.cf_upload_image.project
  region         = google_cloudfunctions_function.cf_upload_image.region
  cloud_function = google_cloudfunctions_function.cf_upload_image.name

  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${google_service_account.microservice_fr.email}"
}

# Enable cloud functions API