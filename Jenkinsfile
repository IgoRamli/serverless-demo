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
                // Install Java
                sh 'apt-get -y update'
                sh 'apt-get -y install default-jdk'
                
                // Install pip requirements
                sh 'python --version'
                sh 'python -m venv env'
                sh 'pip install --upgrade pip'
                sh 'pip install -r app/requirements.txt'
                
                // Install and run Firebase Emulator
                sh 'npm install -g firebase-tools'
                sh 'firebase setup:emulators:firestore'
                sh 'firebase setup:emulators:pubsub'

                // Run tests
                sh 'pip install pytest pytest-cov coverage'
                sh 'firebase emulators:exec --only=firestore,pubsub "pytest --junit-xml=./build/reports.xml --cov=./app ./app/test"'
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
                
                // Build and submit docker
                sh 'sudo docker build ./app -t monolith'
                sh 'sudo docker tag monolith gcr.io/intern-experiment/monolith'
                sh 'sudo docker push gcr.io/intern-experiment/monolith'
            }
        }
    }
}