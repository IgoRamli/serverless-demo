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

#  This is supposed to create Firebase projects and resources. However, it is currently not stable.
#  Uncomment this at your own risk

# resource "google_firebase_project" "default" {
#     provider = google-beta
#     project  = var.project
# }

# resource "google_firebase_web_app" "serverless_store" {
#     provider = google-beta
#     project = var.project
#     display_name = "Serverless Store web app"

#     depends_on = [google_firebase_project.default]
# }

# data "google_firebase_web_app_config" "serverless_store" {
#   provider   = google-beta
#   web_app_id = google_firebase_web_app.serverless_store.app_id
# }

# resource "google_app_engine_application" "firestore" {
#   project     = var.project
#   location_id = "asia-southeast2"
#   database_type = "CLOUD_FIRESTORE"
# }