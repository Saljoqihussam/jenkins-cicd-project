pipeline {
    agent any

    // Requirement: "a commit triggers an automated build"
    // pollSCM checks GitHub every ~2 minutes and builds only if there is a new commit.
    // If your Jenkins is reachable from the internet (e.g. via ngrok), you can replace
    // this with githubPush() and add a webhook in GitHub -> Settings -> Webhooks.
    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        DOCKER_IMAGE = 'hussam160803/jenkins-cicd-api'
        IMAGE_TAG    = "${BUILD_NUMBER}"
        K8S_DEPLOY   = 'student-api'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --pretty=format:"Commit: %h - %s (%an)"'
            }
        }

        stage('Install Dependencies & Test') {
            steps {
                sh '''
                    docker run --rm \
                      --volumes-from "$HOSTNAME" \
                      -w "$WORKSPACE" \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir --default-timeout=120 --retries=10 -r requirements.txt && python -m pytest -v --junitxml=test-results.xml"
                '''
            }
            post {
                always {
                    // Shows a "Test Result" page in Jenkins for each build
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                // Tag with the build number so every build is a unique, traceable image
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest .
                '''
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
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // 'kubeconfig' = a Jenkins credential of type "Secret file"
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl version --client
                        # Replace :latest with this build's tag, then apply
                        sed "s|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|" k8s/deployment.yaml | kubectl apply -f -
                        kubectl apply -f k8s/service.yaml
                        kubectl rollout status deployment/${K8S_DEPLOY} --timeout=180s
                        kubectl get pods,svc -l app=${K8S_DEPLOY} -o wide
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "SUCCESS: ${JOB_NAME} #${BUILD_NUMBER} - tests passed, image ${DOCKER_IMAGE}:${IMAGE_TAG} pushed and deployed to Kubernetes."
            echo "Build URL: ${BUILD_URL}"
            // Bonus (needs the Mailer plugin + SMTP set in Manage Jenkins -> System):
            // mail to: 'your-group@example.com',
            //      subject: "SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
            //      body: "Deployed ${DOCKER_IMAGE}:${IMAGE_TAG}\n${BUILD_URL}"
        }
        failure {
            echo "FAILURE: ${JOB_NAME} #${BUILD_NUMBER} failed. Check the console output: ${BUILD_URL}console"
            // mail to: 'your-group@example.com',
            //      subject: "FAILURE: ${JOB_NAME} #${BUILD_NUMBER}",
            //      body: "Pipeline failed. Logs: ${BUILD_URL}console"
        }
        always {
            echo 'Pipeline execution completed.'
            // Free disk space on the Jenkins host (ignore errors if already removed)
            sh 'docker image rm ${DOCKER_IMAGE}:${IMAGE_TAG} || true'
        }
    }
}
