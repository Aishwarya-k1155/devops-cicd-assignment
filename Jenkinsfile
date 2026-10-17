
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'devops-cicd-app'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub'
                checkout scm
            }
        }

        stage('Build Application') {
            steps {
                echo 'Building the application'
                bat 'dir'
                bat 'python --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                bat 'docker build -t %DOCKER_IMAGE% .'
            }
        }

        stage('Verify Kubernetes') {
            steps {
                echo 'Checking Kubernetes connectivity'
                bat 'kubectl config current-context'
                bat 'kubectl cluster-info'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
