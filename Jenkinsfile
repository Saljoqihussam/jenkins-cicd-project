
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'hussam160803/jenkins-cicd-api'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies & Test') {
            steps {
                sh '''
                    docker run --rm \
                      --volumes-from "$HOSTNAME" \
                      -w "$WORKSPACE" \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt && python -m pytest -v"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed and Docker image pushed!'
        }
        failure {
            echo 'FAILURE: Pipeline failed. Check the console output.'
        }
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
