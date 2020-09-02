resource "kubernetes_config_map" "service_ip" {
  metadata {
    name      = var.gke_configmap_service_ip_name
    namespace = kubernetes_namespace.frontend.metadata[0].name
  }

  data = {
      backend = "http://${var.gke_service_backend_name}.${var.gke_namespace_backend_name}.svc.cluster.local"
      frontend = "http://${var.gke_service_frontend_name}.${var.gke_namespace_frontend_name}.svc.cluster.local"
  }
}

resource "kubernetes_config_map" "frontend" {
  metadata {
    name      = var.gke_configmap_frontend_name
    namespace = kubernetes_namespace.frontend.metadata[0].name
  }

  data = {
      project         = var.project
      bucket          = google_storage_bucket.product_image.name
      firebase-config = "firebase_config.json"
  }
}

resource "kubernetes_config_map" "backend" {
  metadata {
    name      = var.gke_configmap_backend_name
    namespace = kubernetes_namespace.backend.metadata[0].name
  }

  data = {
      project         = var.project
      bucket          = google_storage_bucket.product_image.name
      firebase-config = "firebase_config.json"
      new-product     = google_pubsub_topic.new_product.name
      payment-process = google_pubsub_topic.payment_process.name
  }
}