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
                sh 'firebase emulators:start'

                // Run tests
                sh 'pip install pytest pytest-cov coverage'
                sh 'SCRIPT="pytest --cov-report term --cov=./app ./test"'
                sh 'firebase emulators:exec $SCRIPT'
            }
        }
    }
}