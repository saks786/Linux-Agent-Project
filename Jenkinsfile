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
                echo "🛑 Removing old containers and networks..."
            docker-compose down --remove-orphans || true

            echo "🧹 Pruning unused networks..."
            docker network prune -f || true

            echo "🚀 Starting new containers..."
            docker-compose up -d --build
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'sleep 10'  // wait for db + app to initialize
                sh 'curl -f http://localhost:5000 || (echo "❌ Flask not responding" && exit 1)'
                sh 'curl -f http://localhost:5000/db || (echo "❌ DB connection failed" && exit 1)'
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
