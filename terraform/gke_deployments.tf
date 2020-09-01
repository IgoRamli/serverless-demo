resource "kubernetes_deployment" "frontend" {
    metadata {
        name      = var.gke_deployment_frontend_name
        namespace = kubernetes_namespace.frontend.metadata[0].name
        labels    = var.gke_deployment_frontend_labels
    }

    spec {
        replicas = 2

        selector {
            match_labels = var.gke_deployment_frontend_labels
        }

        template {
            metadata {
                labels = var.gke_deployment_frontend_labels
            }

            spec {
                service_account_name = kubernetes_service_account.frontend.metadata[0].name
                container {
                    image = "gcr.io/${var.project}/frontend"
                    name  = var.gke_container_frontend_name

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
                    env {
                        name       = "GCP_PROJECT"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.frontend.metadata[0].name
                                key  = "project"
                            }
                        }
                    }
                    env {
                        name       = "GCS_BUCKET"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.frontend.metadata[0].name
                                key  = "bucket"
                            }
                        }
                    }
                    env {
                        name       = "FIREBASE_CONFIG"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.frontend.metadata[0].name
                                key  = "firebase-config"
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
        name      = var.gke_deployment_backend_name
        namespace = kubernetes_namespace.backend.metadata[0].name
        labels    = var.gke_deployment_backend_labels
    }

    spec {
        replicas = 3

        selector {
            match_labels = var.gke_deployment_backend_labels
        }

        template {
            metadata {
                labels = var.gke_deployment_backend_labels
            }

            spec {
                service_account_name = kubernetes_service_account.backend.metadata[0].name
                container {
                    image = "gcr.io/${var.project}/backend"
                    name  = var.gke_container_backend_name

                    port {
                        container_port = "80"
                    }

                    env {
                        name  = "PORT"
                        value = "80"
                    }
                    env {
                        name       = "GCP_PROJECT"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.backend.metadata[0].name
                                key  = "project"
                            }
                        }
                    }
                    env {
                        name       = "GCS_BUCKET"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.backend.metadata[0].name
                                key  = "bucket"
                            }
                        }
                    }
                    env {
                        name       = "FIREBASE_CONFIG"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.backend.metadata[0].name
                                key  = "firebase-config"
                            }
                        }
                    }
                    env {
                        name       = "PUBSUB_TOPIC_NEW_PRODUCT"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.backend.metadata[0].name
                                key  = "new-product"
                            }
                        }
                    }
                    env {
                        name       = "PUBSUB_TOPIC_PAYMENT_PROCESS"
                        value_from {
                            config_map_key_ref {
                                name = kubernetes_config_map.backend.metadata[0].name
                                key  = "payment-process"
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

resource "kubernetes_deployment" "loadgen" {
    metadata {
        name      = var.gke_deployment_loadgen_name
        namespace = kubernetes_namespace.frontend.metadata[0].name
        labels    = var.gke_deployment_loadgen_labels
    }

    spec {
        replicas = 1

        selector {
            match_labels = var.gke_deployment_loadgen_labels
        }

        template {
            metadata {
                labels = var.gke_deployment_loadgen_labels
            }

            spec {
                service_account_name = kubernetes_service_account.loadgen.metadata[0].name
                container {
                    image = "gcr.io/${var.project}/frontend"
                    name  = var.gke_container_loadgen_name

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