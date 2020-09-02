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

data "google_client_config" "provider" {}

resource "google_container_cluster" "microservices" {
  project               = var.project
  provider              = google-beta.gb3
  name                  = var.gke_cluster_name
  location              = var.location
  initial_node_count    = 3

  # Enable Workload Identity
  workload_identity_config {
    identity_namespace = "${var.project}.svc.id.goog"
  }

  master_auth {
    username = ""
    password = ""

    client_certificate_config {
      issue_client_certificate = false
    }
  }

  node_config {
    machine_type = "n1-standard-2"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/cloud-platform.read-only",
    ]

    workload_metadata_config {
      node_metadata = "GKE_METADATA_SERVER"
    }
  }
}

provider "kubernetes" {
  load_config_file = false

  host  = "https://${google_container_cluster.microservices.endpoint}"
  token = data.google_client_config.provider.access_token
  cluster_ca_certificate = base64decode(
    google_container_cluster.microservices.master_auth[0].cluster_ca_certificate,
  )
}

resource "kubernetes_namespace" "frontend" {
    metadata {
        name = var.gke_namespace_frontend_name
    }
}
resource "kubernetes_namespace" "backend" {
    metadata {
        name = var.gke_namespace_backend_name
    }
}


resource "kubernetes_service_account" "frontend" {
    metadata {
        name      = var.gke_sa_frontend_name
        namespace = kubernetes_namespace.frontend.metadata[0].name
        annotations = {
            "iam.gke.io/gcp-service-account" = google_service_account.microservice_fr.email
        }
    }
}

resource "kubernetes_service_account" "backend" {
    metadata {
        name      = var.gke_sa_backend_name
        namespace = kubernetes_namespace.backend.metadata[0].name
        annotations = {
            "iam.gke.io/gcp-service-account" = google_service_account.microservice_ba.email
        }
    }
}

resource "kubernetes_service_account" "loadgen" {
    metadata {
        name      = var.gke_sa_loadgen_name
        namespace = kubernetes_namespace.frontend.metadata[0].name
        annotations = {
            "iam.gke.io/gcp-service-account" = google_service_account.loadgen.email
        }
    }
}