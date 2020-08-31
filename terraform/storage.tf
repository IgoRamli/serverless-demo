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

provider "google-beta" {
  project = var.project
  alias   = "gb3"
}

# Storage bucket for storing product images
resource "google_storage_bucket" "product_image" {
  project     = var.project
  name        = "${var.project}-storage"
  location    = var.region

  # delete bucket and contents on destroy.
  force_destroy = true
}

# Storage bucket for storing Cloud Function's source code
resource "google_storage_bucket" "storage_cfunctions" {
  project     = var.project
  name        = "${var.project}-cfunctions"
  location    = var.region

  # delete bucket and contents on destroy.
  force_destroy = true
}

# Storage bucket for storing generated config files
resource "google_storage_bucket" "config" {
  project     = var.project
  name        = "${var.project}-config"
  location    = var.region

  # delete bucket and contents on destroy.
  force_destroy = true
}

# Make image storage publicly available
resource "google_storage_bucket_acl" "product_image_acl" {
  bucket          = google_storage_bucket.product_image.name
  predefined_acl  = "publicRead"
}

# ZIP all source code
data "archive_file" "src_zip"{
  for_each = toset( ["automl", "detect_labels", "pay_with_stripe", "upload_image", "streamEvents"] )

  type        = "zip"
  source_dir = "${path.module}/../../functions/${each.key}"
  output_path = "${path.module}/../../functions/zip/${each.key}.zip"
}


# All Cloud Function's source codes
resource "google_storage_bucket_object" "cfunctions_src" {
  for_each = toset( ["automl", "detect_labels", "pay_with_stripe", "upload_image", "streamEvents"] )

  name   = "${each.key}.zip"
  bucket = google_storage_bucket.storage_cfunctions.name
  source = "${path.module}/../../functions/zip/${each.key}.zip"
}