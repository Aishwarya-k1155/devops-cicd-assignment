
pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
        timeout(time: 15, unit: 'MINUTES')
    }

    parameters {
        string(
            name: 'DOCKER_IMAGE',
            defaultValue: 'cicd-app:1.0',
            description: 'Docker image name and tag to build and deploy'
        )
        string(
            name: 'KUBE_CONTEXT',
            defaultValue: 'docker-desktop',
            description: 'Kubernetes context configured on the Jenkins agent'
        )
    }

    environment {
        KUBECONFIG = 'C:\\ProgramData\\Jenkins\\.jenkins\\.kube\\config'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from the configured Git repository.'
                checkout scm
            }
        }

        stage('Validate Project Files') {
            steps {
                echo 'Checking required application and Kubernetes files.'
                bat 'if not exist app\\app.py exit /b 1'
                bat 'if not exist Dockerfile exit /b 1'
                bat 'if not exist k8s\\deployment.yaml exit /b 1'
                bat 'if not exist k8s\\service.yaml exit /b 1'
                echo 'All required project files are present.'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    if (!params.DOCKER_IMAGE?.trim()) {
                        error('DOCKER_IMAGE is empty. Set it to cicd-app:1.0.')
                    }
                }

                echo 'Building the Docker image.'
                bat 'docker build -t "cicd-app:1.0" .'
                bat 'docker image inspect "cicd-app:1.0"'
            }
        }

        stage('Verify Kubernetes Access') {
            steps {
                script {
                    if (!params.KUBE_CONTEXT?.trim()) {
                        error('KUBE_CONTEXT is empty. Set it to docker-desktop.')
                    }
                }

                echo 'Verifying access to the selected Kubernetes context.'
                bat 'kubectl --kubeconfig="%KUBECONFIG%" --context="%KUBE_CONTEXT%" cluster-info'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Applying the Kubernetes Deployment and Service.'
                bat 'kubectl --kubeconfig="%KUBECONFIG%" --context="%KUBE_CONTEXT%" apply -f k8s\\deployment.yaml'
                bat 'kubectl --kubeconfig="%KUBECONFIG%" --context="%KUBE_CONTEXT%" apply -f k8s\\service.yaml'

                echo 'Setting the image built by this pipeline.'
                bat 'kubectl --kubeconfig="%KUBECONFIG%" --context="%KUBE_CONTEXT%" set image deployment/cicd-app cicd-app=cicd-app:1.0'

                echo 'Restarting the Deployment to use the newly built local image.'
                bat 'kubectl --kubeconfig="%KUBECONFIG%" --context="%KUBE_CONTEXT%" rollout restart deployment/cicd-app'

                echo 'Waiting for the application rollout to complete.'
                bat 'kubectl --kubeconfig="%KUBECONFIG%" --context="%KUBE_CONTEXT%" rollout status deployment/cicd-app --timeout=120s'

                echo 'Displaying the deployed Pods and Service.'
                bat 'kubectl --kubeconfig="%KUBECONFIG%" --context="%KUBE_CONTEXT%" get pods'
                bat 'kubectl --kubeconfig="%KUBECONFIG%" --context="%KUBE_CONTEXT%" get service cicd-app-service'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Build completed and the Kubernetes deployment was verified.'
            echo 'Application endpoint: http://localhost:30080'
        }

        failure {
            echo 'FAILURE: The pipeline did not complete. Review the first failed stage and its console output.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
