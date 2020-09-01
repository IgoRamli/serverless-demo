pipeline {
    agent none
    stages {
        stage('test') {
            agent {
                docker {
                    image 'nikolaik/python-nodejs'
                    args '--user=\"root\"'
                }
            }
            steps {
                sh 'echo "Doing tests on frontend!"'
                sh 'echo "Doing tests on backend!"'
            }
        }
        stage('dockerize') {
            parallel {
                stage('dockerize-frontend'){
                    agent {
                        label 'jenkins-deployer'
                    }
                    when {
                        branch 'master'
                    }
                    environment {
                        GCR_CREDENTIALS = credentials('docker-pusher')
                    }
                    steps {
                        // Login with Service Account
                        sh "sudo gcloud auth activate-service-account ${jenkins-deployer-sa} --key-file=$GCR_CREDENTIALS"
                        sh 'echo "Y" | sudo gcloud auth configure-docker'
                        // Build and submit docker
                        sh 'sudo docker build ./src/frontend -t frontend'
                        sh 'sudo docker tag frontend gcr.io/${project-id}/frontend'
                        sh 'sudo docker push gcr.io/${project-id}/frontend'
                    }
                }
                stage('dockerize-backend'){
                    agent {
                        label 'jenkins-deployer'
                    }
                    when {
                        branch 'master'
                    }
                    environment {
                        GCR_CREDENTIALS = credentials('docker-pusher')
                    }
                    steps {
                        // Login with Service Account
                        sh "sudo gcloud auth activate-service-account ${jenkins-deployer-sa} --key-file=$GCR_CREDENTIALS"
                        sh 'echo "Y" | sudo gcloud auth configure-docker'
                        // Build and submit docker
                        sh 'sudo docker build ./src/backend -t backend'
                        sh 'sudo docker tag backend gcr.io/${project-id}/backend'
                        sh 'sudo docker push gcr.io/${project-id}/backend'
                    }
                }
            }
        }
    }
}