pipeline {
    agent any

    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    pwd
                    ls -la
                    . .venv/bin/activate
                    python -m pytest -q
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withCredentials([string(credentialsId: 'sonar-qube-token', variable: 'SONAR_TOKEN')]) {
                        withSonarQubeEnv('SonarQube') {
                            sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=aceest-fitness-gym -Dsonar.projectName='ACEest Fitness and Gym' -Dsonar.sources=."
                        }
                    }
                }
            }
        }

        
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker --version
                    docker build -t aceest-fitness-gym .
                '''
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {
                    sh '''
                        set -eu
                        export DOCKER_CONFIG="$(mktemp -d)"
                        trap 'rm -rf "$DOCKER_CONFIG"' EXIT

                        IMAGE_REPOSITORY='docker.io/2026ht66002/devops-assignment-2'
                        printf '%s' "$DOCKERHUB_PASSWORD" | docker login docker.io \
                            --username "$DOCKERHUB_USERNAME" --password-stdin
                        docker tag aceest-fitness-gym "$IMAGE_REPOSITORY:latest"
                        docker tag aceest-fitness-gym "$IMAGE_REPOSITORY:$BUILD_NUMBER"
                        docker push "$IMAGE_REPOSITORY:latest"
                        docker push "$IMAGE_REPOSITORY:$BUILD_NUMBER"
                    '''
                }
            }
        }

    }
}
