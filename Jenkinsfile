pipeline {
    agent any
    
    triggers {
        cron('H 6 * * *')   // 每天早上 6 点自动跑
    }
    
    environment {
        USE_MOCK = 'false'
        TEST_ENV = 'dev'
    }
    
    stages {
        stage('Parallel Test') {
            parallel {
                stage('member') {
                    steps {
                        sh '''
                            .venv/bin/pytest Testcase/member-service/ -q --tb=short \
                            --alluredir=allure-results/member || true
                        '''
                    }
                }
                stage('pay') {
                    steps {
                        sh '.venv/bin/pytest Testcase/pay-service/ -q --alluredir=allure-results/pay || true'
                    }
                }
                stage('system') {
                    steps {
                        sh '.venv/bin/pytest Testcase/system-service/ -q --alluredir=allure-results/system || true'
                    }
                }
                stage('trade') {
                    steps {
                        sh '.venv/bin/pytest Testcase/trade-service/ -q --alluredir=allure-results/trade || true'
                    }
                }
                stage('recycle') {
                    steps {
                        sh '.venv/bin/pytest Testcase/recycle-service/ -q --alluredir=allure-results/recycle || true'
                    }
                }
                stage('risk') {
                    steps {
                        sh '.venv/bin/pytest Testcase/risk-service/ -q --alluredir=allure-results/risk || true'
                    }
                }
                stage('product') {
                    steps {
                        sh '.venv/bin/pytest Testcase/product-service/ -q --alluredir=allure-results/product || true'
                    }
                }
                stage('statistics') {
                    steps {
                        sh '.venv/bin/pytest Testcase/statistics-service/ -q --alluredir=allure-results/statistics || true'
                    }
                }
            }
        }
        
        stage('Allure Report') {
            steps {
                allure includeProperties: false, results: [[path: 'allure-results']]
            }
        }
    }
    
    post {
        always {
            // 清理 .pyc 防止干扰
            sh 'find Testcase -name "*.pyc" -delete'
        }
    }
}
