pipeline {
    agent {
        docker {
            image 'python:3.7-slim-buster'
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
                // Install Node.js
                sh 'apt-get -y update'
                sh 'apt-get -y install curl'
                sh 'curl -sL https://deb.nodesource.com/setup_12.x | bash'
                sh 'apt-get -y update'
                sh 'apt-get -y install nodejs npm node-gyp'
                sh 'node -v'
                sh 'npm install npm@latest -g'
                sh 'npm -v'

                // Install and run Firebase Emulator
                sh 'npm install -g firebase-tools'
                sh 'firebase emulators:start'

                // Run tests
                sh 'pip install pytest pytest-cov coverage'
                sh 'pytest --cov-report term --cov=./app ./test'
            }
        }
    }
}