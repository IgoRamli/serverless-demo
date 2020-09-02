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
  account_id   = var.gsa_microservice_ba_id
  display_name = var.gsa_microservice_ba_id
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
  account_id   = var.gsa_microservice_fr_id
  display_name = var.gsa_microservice_fr_id
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
  account_id   = var.gsa_jenkins_id
  display_name = var.gsa_jenkins_id
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
  account_id   = var.gsa_jenkins_deployer_id
  display_name = var.gsa_jenkins_deployer_id
}

resource "google_project_iam_member" "jenkins_storage_object_admin" {
  project   = var.project
  role      = "roles/storage.objectAdmin"
  member    = "serviceAccount:${google_service_account.jenkins_deployer.email}"
}

resource "google_service_account" "loadgen" {
  project      = var.project
  account_id   = var.gsa_microservice_lg_id
  display_name = var.gsa_microservice_lg_id
}

resource "google_project_iam_member" "loadgen_firebase_admin" {
  project   = var.project
  role      = "roles/firebase.admin"
  member    = "serviceAccount:${google_service_account.loadgen.email}"
}

resource "google_service_account_iam_binding" "backend" {
  service_account_id = google_service_account.microservice_ba.name
  role = "roles/iam.workloadIdentityUser"

  members = [
    "serviceAccount:${var.project}.svc.id.goog[${kubernetes_service_account.backend.metadata[0].namespace}/${kubernetes_service_account.backend.metadata[0].name}]",
  ]
}

resource "google_service_account_iam_binding" "frontend" {
  service_account_id = google_service_account.microservice_fr.name
  role = "roles/iam.workloadIdentityUser"

  members = [
    "serviceAccount:${var.project}.svc.id.goog[${kubernetes_service_account.frontend.metadata[0].namespace}/${kubernetes_service_account.frontend.metadata[0].name}]",
  ]
}

resource "google_service_account_iam_binding" "loadgen" {
  service_account_id = google_service_account.loadgen.name
  role = "roles/iam.workloadIdentityUser"

  members = [
    "serviceAccount:${var.project}.svc.id.goog[${kubernetes_service_account.loadgen.metadata[0].namespace}/${kubernetes_service_account.loadgen.metadata[0].name}]",
  ]
}