pipeline {
    agent any

    environment {
        IMAGE_NAME = 'hossam789/nexus-ops'
        KUBECONFIG = '/var/lib/jenkins/.kube/nexus-ops-config'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/hossamelboghdady123-sketch/nexus-ops.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test Application') {
            steps {
                sh '.venv/bin/python -m pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                      -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Docker Hub Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        set +x
                        echo "$DOCKER_TOKEN" | docker login \
                          --username "$DOCKER_USER" --password-stdin

                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    /usr/local/bin/kubectl \
                      set image deployment/nexus-ops \
                      nexus-ops=${IMAGE_NAME}:${BUILD_NUMBER}

                    /usr/local/bin/kubectl \
                      rollout status deployment/nexus-ops \
                      --timeout=180s
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout >/dev/null 2>&1 || true'
        }
        success {
            echo 'NEXUS Ops CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
