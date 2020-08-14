resource "google_cloud_run_service" "default" {
  name     = "monolith"
  location = "asia-east1"
  project  = "intern-experiment"
  autogenerate_revision_name = true

  template {
    spec {
      containers {
        image = "gcr.io/intern-experiment/monolith"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}