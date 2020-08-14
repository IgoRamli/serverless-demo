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
  role      = "roles/logs.logWriter"
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