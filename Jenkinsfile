pipeline {
    agent {
        docker {
            image 'python:3.5.1'
            label 'docker'
        }
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}