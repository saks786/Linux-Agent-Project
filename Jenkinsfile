pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/saks786/Linux-Agent-Project.git'
            }
        }

        stage('Build & Deploy with Docker Compose') {
            steps {
                sh '''
                echo "✅ Checking for docker-buildx plugin..."
                if ! docker buildx version >/dev/null 2>&1; then
                  echo "⚠️ buildx not found. Installing..."
                  sudo mkdir -p /usr/local/lib/docker/cli-plugins/
                  sudo curl -L https://github.com/docker/buildx/releases/latest/download/buildx-linux-amd64 \
                    -o /usr/local/lib/docker/cli-plugins/docker-buildx
                  sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx
                  echo "✅ buildx installed!"
                fi

                echo "✅ Checking for docker compose plugin..."
                if ! docker compose version >/dev/null 2>&1; then
                  echo "⚠️ docker compose plugin not found. Installing..."
                  sudo apt-get update -y
                  sudo apt-get install -y docker-compose-plugin
                  echo "✅ docker compose plugin installed!"
                fi

                echo "🚀 Stopping old containers..."
                docker compose down || true

                echo "🚀 Building & starting containers..."
                docker compose up -d --build
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                echo "🔍 Checking running containers..."
                docker ps

                echo "🔍 Checking logs..."
                docker compose logs --tail=20
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build & Deploy successful!'
        }
        failure {
            echo '❌ Build/Deploy failed! Check logs.'
        }
    }
}

