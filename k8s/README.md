# Serverless Store Microservices Architecture

Serverless Store's Web Application follows a basic microservices architecture. There are two microservices that make up the service: Frontend and Backend. To ensure smooth orchestration between the two, Serverless Store uses Google Kubernetes Engine to host all microservices.

## Overview

Both frontend and backend runs on Kubernetes as deployments. Each deployment have different Docker images and different services that exposes them. From those two, only the frontend microservice that will be exposed to the user using a `LoadBalancer`. In order to connect with the backend microservice, frontend will uses backend's `ClusterIP` to communicate internally.

Aside from the two webapp microservices, there is a third microservice: the load generator. Load generator (or loadgen) is an independent deployment that simulates user traffic. It will periodically make requests to both frontend and backend to generate user data.

## Architecture

![architecture_k8s](../../docs/architecture_k8s.png)

## Setting up Google Kubernetes Engine Manually

This repository uses Terraform to set up Kubernetes Engine. If you prefer to set up Kubernetes manually, you can follow this guide:

### Prerequisite

This tutorial assumes that you have completed the first 7 steps of the main set-up guide. You also need `kubectl` in your local machine. You can use Cloud Shell provided by Google, or you can download it manually.

### Step 1: Set up Kubernetes Cluster

The first thing you need to do is to create a new cluster.

- Go to [Kubernetes Engine](https://console.cloud.google.com/kubernetes/list) and click **Create Cluster**.
- Write down `microservices` as your cluster name.
- Select the cluster location of your choice.
- Go to **Security** tab, and check the **Enable Workload Identity** list.
- Leave all of the other field with their default values, and click **Create**
- Wait a few minutes. Your cluster will be provisioned shortly!

### Step 2: Create Google Service Accounts

Each microservice in your cluster will require special service accounts in order to function normally. This can be achieved with Google Service Accounts.

- Go to [IAM & Admin Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) and click **Create Service Account**.
- Write down `microservice-ba` as the name of your service account. This account will grant necessary permission to your backend pods.
- Click **Create**
- In the role form, add these role IDs in the list:
  - `cloudtrace.admin`
  - `datastore.user`
  - `pubsub.publisher`
  - `storage.objectViewer`
- Click **Create**
- Leave the user access field empty, and click **Create**
- You have successfully created your backend's GSA!
- Repeat the previous steps to create `microservice-fr` service account. This service account must have these roles:
  - `firebase.admin`
  - `logging.logWriter`
  - `storage.objectAdmin`
- Repeat the previous steps to create `loadgen` service account. Add these roles:
  - `firebase.admin`

### Step 3: Deploy your Kubernetes Components using kubectl

Inside a Kubernetes cluster, there exists multiple components, such as namespaces, Kubernetes Service Accounts, Services, Deployments, etc. In order to make configuring these components a bit easier, we have created several manifests file located in this README's folder.

- Make sure that you have kubectl installed by running `kubectl version`
- Go to each deployment files (`deployments/frontend.yaml`, `deployments/backend.yaml`, `deployments/loadgen.yaml`), and change the image name to their appropriate location. It should be something like `gcr.io/YOUR_PROEJCT_NAME]/frontend`, `gcr.io/YOUR_PROJECT_NAME]/backend`, and `gcr.io/YOUR_PROEJCT_NAME]/loadgen`)
- Connect your `kubectl` with your GKE cluster. This can be done by clicking **Connect** at your cluster in the Kubernetes Engine cluster list, and then run the given command in your local machine.
- Run these commands in this folder (`/k8s/microservices`) and with the correct ordering:
  - `kubectl apply -f namespaces/frontend.yaml`
  - `kubectl apply -f namespaces/backend.yaml`
  - `kubectl apply -f namespaces/loadgen.yaml`
  - `kubectl apply -f configmaps/service-ip.yaml`
  - `kubectl apply -f serviceaccounts/frontend.yaml`
  - `kubectl apply -f serviceaccounts/backend.yaml`
  - `kubectl apply -f serviceaccounts/loadgen.yaml`
  - `kubectl apply -f deployments/frontend.yaml`
  - `kubectl apply -f deployments/backend.yaml`
  - `kubectl apply -f deployments/loadgen.yaml`
  - `kubectl apply -f services/frontend.yaml`
  - `kubectl apply -f services/backend.yaml`
  - `kubectl apply -f services/loadgen.yaml`
- Check that everything has been set up correctly by going to [Kubernetes Engine](https://console.cloud.google.com/kubernetes) and check the **Workload**, **Service & Ingress**, and other tabs.

### Step 4: Connect your Google Service Account to your Kubernetes Service Account

Each microservice module deployed on your Kubernetes cluster requires specific permission to run properly (e.g. Reading Cloud Storage objects requires `Cloud Storage Viewer` role). These roles are defined using Google Service Account. However, Kubernetes deployment uses Kubernetes Service Account for authorization. Therefore, you will need to link your GSA to KSA.

- Run the command `gcloud iam service-accounts add-iam-policy-binding --role roles/iam.workloadIdentityUser --member "serviceAccount:microservices.svc.id.goog[frontend/frontend-sa]" microservice-fr@[GCP_PROJECT_NAME].iam.gserviceaccount.com`. This command links your front end GSA (microservice-fr) to your front end's KSA (frontend-sa). Remember to replace `[GCP_PROJECT_NAME]` with your actual project name.
- Run the command `gcloud iam service-accounts add-iam-policy-binding --role roles/iam.workloadIdentityUser --member "serviceAccount:microservices.svc.id.goog[backend/backend-sa]" microservice-ba@[GCP_PROJECT_NAME].iam.gserviceaccount.com`. This command links your back end GSA (microservice-ba) to your back end's KSA (backend-sa). Remember to replace `[GCP_PROJECT_NAME]` with your actual project name.
- Run the command `gcloud iam service-accounts add-iam-policy-binding --role roles/iam.workloadIdentityUser --member "serviceAccount:microservices.svc.id.goog[loadgen/loadgen-sa]" loadgen@[GCP_PROJECT_NAME].iam.gserviceaccount.com`. This command links your load generator GSA (loadgen) to your load generator's KSA (loadgen-sa). Remember to replace `[GCP_PROJECT_NAME]` with your actual project name.

For more information on using Workload Identity, refer to [this documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity).
