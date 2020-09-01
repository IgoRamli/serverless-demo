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
 
resource "google_service_account" "microservice_ba" {
  project      = var.project
  account_id   = "microservice-ba"
  display_name = "microservice-ba"
}

resource "google_project_iam_member" "trace_admin" {
  project   = var.project
  role      = "roles/cloudtrace.admin"
  member    = "serviceAccount:${google_service_account.microservice_ba.email}"
}

resource "google_project_iam_member" "datastore_user" {
  project   = var.project
  role      = "roles/datastore.user"
  member    = "serviceAccount:${google_service_account.microservice_ba.email}"
}

resource "google_project_iam_member" "pubsub_publisher" {
  project   = var.project
  role      = "roles/pubsub.publisher"
  member    = "serviceAccount:${google_service_account.microservice_ba.email}"
}

resource "google_project_iam_member" "storage_object_viewer" {
  project   = var.project
  role      = "roles/storage.objectViewer"
  member    = "serviceAccount:${google_service_account.microservice_ba.email}"
}

resource "google_service_account" "microservice_fr" {
  project      = var.project
  account_id   = "microservice-fr"
  display_name = "microservice-fr"
}

resource "google_project_iam_member" "firebase_admin" {
  project   = var.project
  role      = "roles/firebase.admin"
  member    = "serviceAccount:${google_service_account.microservice_fr.email}"
}

resource "google_project_iam_member" "logs_writer" {
  project   = var.project
  role      = "roles/logging.logWriter"
  member    = "serviceAccount:${google_service_account.microservice_fr.email}"
}

resource "google_project_iam_member" "storage_object_admin" {
  project   = var.project
  role      = "roles/storage.objectAdmin"
  member    = "serviceAccount:${google_service_account.microservice_fr.email}"
}

resource "google_service_account" "jenkins" {
  project      = var.project
  account_id   = "jenkins"
  display_name = "jenkins"
}

resource "google_project_iam_member" "jenkins_compute_instance_admin" {
  project   = var.project
  role      = "roles/compute.instanceAdmin.v1"
  member    = "serviceAccount:${google_service_account.jenkins.email}"
}

resource "google_project_iam_member" "jenkins_compute_network_admin" {
  project   = var.project
  role      = "roles/compute.networkAdmin"
  member    = "serviceAccount:${google_service_account.jenkins.email}"
}

resource "google_project_iam_member" "jenkins_compute_security_admin" {
  project   = var.project
  role      = "roles/compute.securityAdmin"
  member    = "serviceAccount:${google_service_account.jenkins.email}"
}

resource "google_project_iam_member" "jenkins_sa_user" {
  project   = var.project
  role      = "roles/iam.serviceAccountUser"
  member    = "serviceAccount:${google_service_account.jenkins.email}"
}

resource "google_service_account" "jenkins_deployer" {
  project      = var.project
  account_id   = "jenkins-deployer"
  display_name = "jenkins-deployer"
}

resource "google_project_iam_member" "jenkins_storage_object_admin" {
  project   = var.project
  role      = "roles/storage.objectAdmin"
  member    = "serviceAccount:${google_service_account.jenkins_deployer.email}"
}

resource "google_service_account" "loadgen" {
  project      = var.project
  account_id   = "loadgen"
  display_name = "loadgen"
}

resource "google_project_iam_member" "loadgen_firebase_admin" {
  project   = var.project
  role      = "roles/firebase.admin"
  member    = "serviceAccount:${google_service_account.loadgen.email}"
}