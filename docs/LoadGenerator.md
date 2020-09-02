# Locust as Load Generator for Serverless Store

Load testing is an integral part of software development. Our infrastructure is ought to sustain heavy user traffic. Testing this requirement with no initial customer base is tricky. For thei problem, Serverless Store uses load testing framework Locust to generate user traffic periodically (1 request every 1-10 seconds). This load testing showcases the scaability of Google Cloud solutions, as well as generating user data for our insight extraction tools.

## Architecture

Locust load generator runs as a single deployment inside our Kubernetes Cluster. This load generator interacts with both frontend and backend internally. Load generator tries to simulate user behaviour as accurately as possible, only performing actions directly through back end only when its absolutely necessary (e.g. when an action requires user to login via Firebase Authentication).

![architecture_loadgen](architecture_k8s.png)

### Set Up Guide

For the guide on installing load generator, follow the main set-up guide. If you prefer to install everything manually (not recommended), you can follow the guide for [setting up Kubernetes](../k8s/microservices/README.md).
