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

variable "bq_dataset" {
    type = string
}

variable "bq_table" {
    type = string
}

variable "cf_automl_name" {
    type = string
}
variable "cf_detect_labels_name" {
    type = string
}
variable "cf_pay_with_stripe_name" {
    type = string
}
variable "cf_streamEvents_name" {
    type = string
}
variable "cf_upload_image_name" {
    type = string
}

variable "gke_cluster_name" {
    type = string
}
variable "gke_namespace_frontend_name" {
    type = string
}
variable "gke_namespace_backend_name" {
    type = string
}
variable "gke_sa_frontend_name" {
    type = string
}
variable "gke_sa_backend_name" {
    type = string
}
variable "gke_sa_loadgen_name" {
    type = string
}

variable "gke_configmap_service_ip_name" {
    type = string
}
variable "gke_configmap_frontend_name" {
    type = string
}
variable "gke_configmap_backend_name" {
    type = string
}

variable "gke_deployment_frontend_name" {
    type = string
}
variable "gke_deployment_frontend_labels" {
    type = map
}
variable "gke_deployment_backend_name" {
    type = string
}
variable "gke_deployment_backend_labels" {
    type = map
}
variable "gke_deployment_loadgen_name" {
    type = string
}
variable "gke_deployment_loadgen_labels" {
    type = map
}
variable "gke_container_frontend_name" {
    type = string
}
variable "gke_container_backend_name" {
    type = string
}
variable "gke_container_loadgen_name" {
    type = string
}
variable "gke_service_frontend_name" {
    type = string
}
variable "gke_service_backend_name" {
    type = string
}

variable "pubsub_topic_new_product_name" {
    type = string
}
variable "pubsub_topic_payment_process_name" {
    type = string
}
variable "pubsub_topic_payment_completion_name" {
    type = string
}

variable "gsa_microservice_ba_id" {
    type = string
}
variable "gsa_microservice_fr_id" {
    type = string
}
variable "gsa_microservice_lg_id" {
    type = string
}
variable "gsa_jenkins_id" {
    type = string
}
variable "gsa_jenkins_deployer_id" {
    type = string
}

variable "gcs_product_image_suffix" {
    type = string
}
variable "gcs_cfunctions_suffix" {
    type = string
}
variable "gcs_config_suffix" {
    type = string
}