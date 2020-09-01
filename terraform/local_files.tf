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
 
data "template_file" "function_env_vars" {
    template = "${file("${path.module}/function_env_vars_template.tpl")}"
    vars     = {
        automl_model_id                 = var.automl_model_id
        gcs_bucket                      = google_storage_bucket.product_image.name
        stripe_api_key                  = var.stripe_api_key
        pubsub_topic_payment_completion = google_pubsub_topic.payment_completion.name
        sendgrid_api_key                = var.sendgrid_api_key
    }
}

resource "local_file" "function_env_vars" {
    content  = data.template_file.function_env_vars.rendered
    filename = "${path.module}/../extras/cloudbuild/functions_env_vars.yaml"
}

data "template_file" "Jenkinsfile" {
    template = "${file("${path.module}/Jenkinsfile_template.tpl")}"
    vars     = {
        project-id          = var.project
        jenkins-deployer-sa = google_service_account.jenkins_deployer.email
    }
}

resource "local_file" "Jenkinsfile" {
    content  = data.template_file.Jenkinsfile.rendered
    filename = "${path.module}/../Jenkinsfile"
}