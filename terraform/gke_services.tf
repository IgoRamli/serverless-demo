resource "kubernetes_service" "frontend" {
    metadata {
        name      = var.gke_service_frontend_name
        namespace = kubernetes_namespace.frontend.metadata[0].name
    }
    spec {
        selector = var.gke_deployment_frontend_labels
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
        name      = var.gke_service_backend_name
        namespace = kubernetes_namespace.backend.metadata[0].name
    }
    spec {
        selector = var.gke_deployment_backend_labels
        port {
            protocol    = "TCP"
            port        = 80
            target_port = 80
        }

        type = "ClusterIP"
    }
}