
pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
            args '-u root'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python --version
                    pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'python -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: All tests passed!'
        }
        failure {
            echo 'FAILURE: Pipeline failed. Check the logs.'
        }
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
