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
  name                  = "microservices"
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
        name = "frontend"
    }
}
resource "kubernetes_namespace" "backend" {
    metadata {
        name = "backend"
    }
}


resource "kubernetes_service_account" "frontend" {
    metadata {
        name      = "frontend-sa"
        namespace = kubernetes_namespace.frontend.metadata[0].name
        annotations = {
            "iam.gke.io/gcp-service-account" = google_service_account.microservice_fr.email
        }
    }
}

resource "kubernetes_service_account" "backend" {
    metadata {
        name      = "backend-sa"
        namespace = kubernetes_namespace.backend.metadata[0].name
        annotations = {
            "iam.gke.io/gcp-service-account" = google_service_account.microservice_ba.email
        }
    }
}

resource "kubernetes_service_account" "loadgen" {
    metadata {
        name      = "loadgen-sa"
        namespace = kubernetes_namespace.frontend.metadata[0].name
        annotations = {
            "iam.gke.io/gcp-service-account" = google_service_account.loadgen.email
        }
    }
}

resource "kubernetes_config_map" "service_ip" {
  metadata {
    name      = "service-ip"
    namespace = kubernetes_namespace.frontend.metadata[0].name
  }

  data = {
      backend = "http://${kubernetes_service.backend.metadata[0].name}.${kubernetes_namespace.backend.metadata[0].name}.svc.cluster.local"
      frontend = "http://${kubernetes_service.frontend.metadata[0].name}.${kubernetes_namespace.frontend.metadata[0].name}.svc.cluster.local"
  }
}

resource "kubernetes_service" "frontend" {
    metadata {
        name      = "frontend"
        namespace = kubernetes_namespace.frontend.metadata[0].name
    }
    spec {
        selector = {
            app = "${kubernetes_deployment.frontend.metadata.0.labels.app}"
        }
        port {
            protocol    = "TCP"
            port        = 80
            target_port = 80
        }

        type = "LoadBalancer"
    }
}

resource "kubernetes_service" "backend" {
    metadata {
        name      = "backend"
        namespace = kubernetes_namespace.backend.metadata[0].name
    }
    spec {
        selector = {
            app = "${kubernetes_deployment.backend.metadata.0.labels.app}"
        }
        port {
            protocol    = "TCP"
            port        = 80
            target_port = 80
        }

        type = "ClusterIP"
    }
}

resource "kubernetes_deployment" "frontend" {
    metadata {
        name      = "frontend"
        namespace = kubernetes_namespace.frontend.metadata[0].name
        labels    = {
            app = "frontend"
        }
    }

    spec {
        replicas = 2

        selector {
            match_labels = {
                app = "frontend"
            }
        }

        template {
            metadata {
                labels = {
                    app = "frontend"
                }
            }

            spec {
                service_account_name = kubernetes_service_account.frontend.metadata[0].name
                container {
                    image = "gcr.io/${var.project}/frontend"
                    name  = "example"

                    port {
                        container_port = "80"
                    }

                    env {
                        name  = "PORT"
                        value = "80"
                    }
                    env {
                        name       = "BACKEND_URL"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.service_ip.metadata[0].name
                                key  = "backend"
                            }
                        }
                    }

                    resources {
                        limits {
                            cpu    = "0.5"
                            memory = "512Mi"
                        }
                        requests {
                            cpu    = "250m"
                            memory = "50Mi"
                        }
                    }
                }
            }
        }
    }
}

resource "kubernetes_deployment" "backend" {
    metadata {
        name      = "backend"
        namespace = kubernetes_namespace.backend.metadata[0].name
        labels    = {
            app = "backend"
        }
    }

    spec {
        replicas = 3

        selector {
            match_labels = {
                app = "backend"
            }
        }

        template {
            metadata {
                labels = {
                    app = "backend"
                }
            }

            spec {
                service_account_name = kubernetes_service_account.backend.metadata[0].name
                container {
                    image = "gcr.io/${var.project}/backend"
                    name  = "backend"

                    port {
                        container_port = "80"
                    }

                    env {
                        name  = "PORT"
                        value = "80"
                    }

                    resources {
                        limits {
                            cpu    = "0.5"
                            memory = "512Mi"
                        }
                        requests {
                            cpu    = "250m"
                            memory = "50Mi"
                        }
                    }
                }
            }
        }
    }
}

resource "kubernetes_deployment" "loadgen" {
    metadata {
        name      = "loadgen"
        namespace = kubernetes_namespace.frontend.metadata[0].name
        labels    = {
            app = "loadgen"
        }
    }

    spec {
        replicas = 1

        selector {
            match_labels = {
                app = "loadgen"
            }
        }

        template {
            metadata {
                labels = {
                    app = "loadgen"
                }
            }

            spec {
                service_account_name = kubernetes_service_account.loadgen.metadata[0].name
                container {
                    image = "gcr.io/${var.project}/loadgen"
                    name  = "loadgen"

                    env {
                        name       = "BACKEND_URL"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.service_ip.metadata[0].name
                                key  = "backend"
                            }
                        }
                    }
                    env {
                        name       = "FRONTEND_ADDR"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.service_ip.metadata[0].name
                                key  = "frontend"
                            }
                        }
                    }

                    resources {
                        limits {
                            cpu    = "0.5"
                            memory = "512Mi"
                        }
                        requests {
                            cpu    = "250m"
                            memory = "50Mi"
                        }
                    }
                }
            }
        }
    }
}