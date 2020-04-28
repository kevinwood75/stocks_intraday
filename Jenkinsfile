node('appserver'){
  try {

    notifyStarted()

    stage('Git Checkout'){
        git credentialsId: 'kevinwood75', url: 'https://github.com/kevinwood75/stocks_intraday.git', branch: 'master'
    }

    stage('Remove old Container release'){
        sh 'docker-compose down'
    }

    stage('Build Docker Image'){
        sh 'docker-compose build'
    }
    stage('Push Docker Image'){
        withCredentials([string(credentialsId: 'docker-pwd', variable: 'dockerhub')]) {
           sh "docker login -u kwood475 -p ${dockerhub}"
        }
        sh 'docker push kwood475/stockintraday:1.0.0'
    }

    stage('Release Container on Server'){
        sh 'docker-compose up -d'

    }
    notifySuccessful()
  } catch (e) {
      currentBuild.result = "FAILED"
      notifyFailed()
      throw e
  }
}

def notifyStarted() {
  slackSend (color: '#FFFF00', message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

def notifySuccessful() {
  slackSend (color: '#00FF00', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

def notifyFailed() {
  slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}
