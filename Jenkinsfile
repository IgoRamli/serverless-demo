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
                parallel (
                    "frontend": {
                        sh "Pretend I'm doing tests on frontend!"
                    },
                    "backend": {
                        sh "Pretend I'm doing tests on backend!"
                    }
                )
            }
        }
        stage('dockerize') {
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
                sh "sudo gcloud auth activate-service-account jenkins-gcr-credentials@intern-experiment.iam.gserviceaccount.com --key-file=$GCR_CREDENTIALS"
                sh 'echo "Y" | sudo gcloud auth configure-docker'
                parallel (
                    "frontend": {
                        // Build and submit docker
                        sh 'sudo docker build ./src/frontend -t frontend'
                        sh 'sudo docker tag frontend gcr.io/intern-experiment/frontend'
                        sh 'sudo docker push gcr.io/intern-experiment/frontend'
                    },
                    "backend": {
                        // Build and submit docker
                        sh 'sudo docker build ./src/backend -t backend'
                        sh 'sudo docker tag backend gcr.io/intern-experiment/backend'
                        sh 'sudo docker push gcr.io/intern-experiment/backend'
                    }
                )
            }
        }
    }
}