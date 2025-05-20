# Flask Backend Server

Jenkins CI/CD 파이프라인에서 무중단 배포 테스트를 위한 Flask 백엔드 서버입니다.

## 기술 스택

- Python 3.x
- Flask 3.0.3
- PyMySQL (선택적)
- MySQL 8.0 (선택적)
- Docker

## 프로젝트 구조

```
flaskserver/
├── app.py
├── requirements.txt
└── Dockerfile
```

## 환경 변수

서버 실행에 필요한 환경 변수:

- `PORT`: 서버 포트
- `USE_DB`: 데이터베이스 사용 여부 (true/false, 기본값: true)
- `MYSQL_HOST`: MySQL 호스트 (USE_DB가 true일 때만 필요)
- `MYSQL_USER`: MySQL 사용자 (USE_DB가 true일 때만 필요)
- `MYSQL_PASSWORD`: MySQL 비밀번호 (USE_DB가 true일 때만 필요)
- `MYSQL_DATABASE`: MySQL 데이터베이스 (USE_DB가 true일 때만 필요)

## Jenkins 파이프라인 설정

Jenkins 파이프라인에서 다음과 같이 환경 변수를 설정하여 사용합니다:

```groovy
pipeline {
    environment {
        PORT = '5000'
        USE_DB = 'true'  // 또는 'false'로 설정하여 데이터베이스 비활성화
        MYSQL_HOST = 'mysql'  // USE_DB가 true일 때만 필요
        MYSQL_USER = 'root'   // USE_DB가 true일 때만 필요
        MYSQL_PASSWORD = credentials('mysql-password')  // USE_DB가 true일 때만 필요
        MYSQL_DATABASE = 'test_db'  // USE_DB가 true일 때만 필요
    }
    stages {
        stage('Deploy') {
            steps {
                sh '''
                    docker build -t flask-backend .
                    docker run -d \
                      -p ${PORT}:${PORT} \
                      -e PORT=${PORT} \
                      -e USE_DB=${USE_DB} \
                      -e MYSQL_HOST=${MYSQL_HOST} \
                      -e MYSQL_USER=${MYSQL_USER} \
                      -e MYSQL_PASSWORD=${MYSQL_PASSWORD} \
                      -e MYSQL_DATABASE=${MYSQL_DATABASE} \
                      flask-backend
                '''
            }
        }
    }
}
```

## API 엔드포인트

- `GET /`: 서버 상태 확인 (데이터베이스 활성화 여부 포함)
- `GET /health`: 서버 및 데이터베이스 상태 확인
- `GET /db-test`: MySQL 연결 테스트 (USE_DB가 true일 때만 사용 가능)

## 데이터베이스 연결 테스트

```bash
# 데이터베이스가 활성화된 경우
curl http://localhost:${PORT}/db-test

# 데이터베이스가 비활성화된 경우
curl http://localhost:${PORT}/db-test  # 400 에러 반환
```
