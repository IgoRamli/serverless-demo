pipeline {
    agent {
        docker {
            image 'nikolaik/python-nodejs'
            args '--user=\"root\"'
        }
    }
    stages {
        stage('build') {
            steps {
                // Install Java
                sh 'apt-get -y update'
                sh 'apt-get -y install default-jdk'
                
                // Install pip requirements
                sh 'python --version'
                sh 'python -m venv env'
                sh 'pip install --upgrade pip'
                sh 'pip install -r app/requirements.txt'
            }
        }
        stage('test') {
            steps {
                // Install and run Firebase Emulator
                sh 'npm install -g firebase-tools'
                sh 'firebase setup:emulators:firestore'
                sh 'firebase setup:emulators:pubsub'

                // Run tests
                sh 'pip install pytest pytest-cov coverage'
                sh 'firebase emulators:exec --only=firestore,pubsub \"pytest --cov-report term --cov=./app ./app/test\"'
            }
        }
    }
}