# Continous Deployment using Jenkins

Google Cloud Platform provides Jenkins as a CI/CD solution for our project. In the `Jenkinsfile` included in this repository, Serverless Store uses Jenkins to automate build, test, and submit Docker images to Google Container Registry. You can use Terraform or Spinnaker to deploy those images to Kubernetes deployment.

## Overview

Jenkins is a Continoud Integration tool that focuses on building projects. Much like other CI/CD tools such as GitLab or GitHub CI/CD, Jenkins is capable of running a pipeline - a set of commands that is executed in stages - and publishing it's result either on a web interface, or on the source control.

Jenkins runs as a standalone application in it's own process. This means running in a machine 24/7. To achieve this, Jenkins is usually run inside a server or a virtual machine in a cloud provider.

Jenkins is very customizable due to it's abundance of plugins. This makes Jenkins a preferrable option for CI/CD when working with various cloud providers. With the correct tools, Jenkins can work with your cloud provider to provision multiple VMs to run your pipeline.

Jenkins runs on pipelines. When a pipeline is triggered, it is run on Jenkin's main machine called "Master agent". This agent manages the overall pipeline execution.

To execute stages, Jenkin's master agent can call multiple stage agents to run stages for it. Each stage agents runs exactly one stage (unless there are multiple stages with the same agent configuration. In that case, Jenkins may reuse it's stage agents).

For our development purpose, stage agents is a Virtual Machine that is provisioned by Google Cloud. Because stage agents is a Virtual Machine, we can use our custom machine image to run stages.

Serverless Store's development pipeline contains two stages: `test` and `dockerize`. Testing stage will be run in a docker with Python and NodeJS pre-installed. Dockerize stage is the stage where docker images are built and pushed to GCR. Because `docker` requires a daemon to run, we will run a custom stage agent with custom machine image to build the docker image. This custom image will have GCloud SDK pre-installed, to make image pushing easier.

## Setting Up Jenkins for Serverless Store

Setting up Jenkins in a Google Cloud project is easy. GCP Deloyment Manager will automatically build a VM with Jenkins installed for you. Configuring Jenkins to run our pipeline, however, is a bit more tricky.

### Step 1: Deploy Jenkins

- Go to [Deployment Manager](onsole.cloud.google.com/dm/deployments), click **Deploy Marketplace Solutions**.
- Search and choose for "Jenkins (Google Click to Deploy)".
- Click **Launch**.
- Give your Jenkins deployment a name and location.
- Leave the rest of the field and click **Deploy**.
- Your Jenkins deployment should be running in a few minutes.
- Write down the IP address, username and password for your Jenkins deployment.
- Go to the specified IP Address, and try to login with your initial account.
