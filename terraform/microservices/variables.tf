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
 
variable "project" {
    type    = string
}

variable "location" {
    type    = string
    default = "asia-east1-a"
}

variable "region" {
    type    = string
    default = "asia-east1"
}

variable "cfunction_region" {
    type    = string
    default = "us-central1"
}

variable "automl_model_id" {
    type    = string
}

variable "stripe_api_key" {
    type    = string
}

variable "sendgrid_api_key" {
    type    = string
}