pipeline {
  agent {
    docker {
      image 'continuumio/anaconda'
    }
    
  }
  stages {
    stage('Build') {
      steps {
        checkout scm
        echo 'Creation python environment'
        sh 'make create_env'
        sh 'source activate object-detection'
      }
    }
    stage('Test') {
      steps {
        echo 'Calling make test script'
        sh 'make test || true'
      }
    }
    stage('Deploy - Staging') {
      when {
        expression {
          currentBuild.result == null || currentBuild.result == 'SUCCESS'
        }
        
      }
      steps {
        echo 'Placeholder: Deploying to staging/dev'
      }
    }
    stage('Sanity check') {
      steps {
        input 'Does the staging environment look ok?'
      }
    }
    stage('Deploy - Production') {
      steps {
        echo 'Placeholder: Deploying to prod'
      }
    }
  }
  post {
    always {
      echo 'The job has finished.'
      
    }
    
    success {
      slackSend(channel: '#ai-nsf-jenkins-jobs', color: 'good', message: "The pipeline ${currentBuild.fillDisplayName} completed successfully.")
      
    }
    
    unstable {
      slackSend(channel: '#ai-nsf-jenkins-jobs', color: 'warning', message: "The pipeline ${currentBuild.fillDisplayName} is unstable. Check it out here: ${env.BUILD_URL}")
      
    }
    
    failure {
      slackSend(channel: '#ai-nsf-jenkins-jobs', color: 'danger', message: "@all The pipeline ${currentBuild.fillDisplayName} has failed! Check it out here: ${env.BUILD_URL}")
      
    }
    
  }
}