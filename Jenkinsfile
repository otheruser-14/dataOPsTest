pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Project') {
            steps {
                sh '''
                    echo "Verification du projet DataOps/MLOps"

                    test -f docker-compose.yml
                    test -f api/Dockerfile
                    test -f api/requirements.txt

                    echo "Structure du projet OK"
                '''
            }
        }

        stage('Verify Git') {
            steps {
                sh '''
                    git log -1 --oneline
                    echo "Git verification OK"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline CI termine avec succes !'
        }

        failure {
            echo 'Pipeline CI en echec !'
        }
    }
}
