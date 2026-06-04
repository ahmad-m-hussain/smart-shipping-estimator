pipeline {

    agent any

    environment {
        IMAGE_NAME      = 'shipping-app'
        CONTAINER_NAME  = 'shipping-container'
        HOST_PORT       = '5000'
        CONTAINER_PORT  = '5000'
    }

    stages {

        // ── Stage 1: Checkout ────────────────────────────────────────────────
        stage('Checkout SCM') {
            steps {
                echo '>>> Pulling latest code from source control...'
                checkout scm
            }
        }

        // ── Stage 2: Build Docker Image ──────────────────────────────────────
        stage('Build Docker Image') {
            steps {
                echo ">>> Building Docker image: ${IMAGE_NAME}..."
                sh 'docker build -t ${IMAGE_NAME} .'
                echo ">>> Image '${IMAGE_NAME}' built successfully."
            }
        }

        // ── Stage 3: Deploy Container ────────────────────────────────────────
        stage('Deploy Container') {
            steps {
                echo ">>> Checking for existing container: ${CONTAINER_NAME}..."

                // Stop the container if running, then remove it if it exists.
                // '|| true' prevents the pipeline from failing if nothing is found.
                sh '''
                    docker stop  ${CONTAINER_NAME} || true
                    docker rm    ${CONTAINER_NAME} || true
                '''

                echo ">>> Starting new container: ${CONTAINER_NAME}..."
                sh '''
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${HOST_PORT}:${CONTAINER_PORT} \
                        --restart unless-stopped \
                        ${IMAGE_NAME}
                '''

                echo ">>> Container '${CONTAINER_NAME}' is live on port ${HOST_PORT}."
            }
        }
    }

    // ── Post-Pipeline Notifications ──────────────────────────────────────────
    post {
        success {
            echo '>>> Pipeline completed successfully. Smart Shipping Estimator is running!'
        }
        failure {
            echo '>>> Pipeline failed. Please check the logs above for details.'
        }
    }
}
