pipeline {
    agent { label 'linux' }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging', 'prod'], description: 'Deploy environment')
    }

    environment {
        COMPOSE_PROJECT_NAME = "linux-agent-${params.DEPLOY_ENV}"
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                git branch: "${params.BRANCH}", url: 'https://github.com/saks786/Linux-Agent-Project.git'
            }
        }

        stage('Build & Deploy with Docker Compose') {
            steps {
                sh '''
                echo "🛑 Removing old postgres-db container if it exists..."
            docker rm -f postgres-db || true

            echo "⬇️ Shutting down old stack..."
            docker-compose down || true

            echo "🚀 Starting new containers..."
            docker-compose up -d --build
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                 echo "⏳ Waiting for Flask to start..."
            sleep 10
            curl -f http://localhost:8000 || { echo "❌ Flask not responding on port 8000"; exit 1; }
            echo "✅ Flask app is up and running on port 8000!"
            }
        }
    }

    post {
        success {
            echo "✅ App + Postgres deployed successfully at http://<agent-ip>:5000"
        }
        failure {
            echo "❌ Build/Deploy failed! Check logs."
        }
    }
}

