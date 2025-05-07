# Flask Backend Server

간단한 Flask 백엔드 서버입니다.

## 기술 스택

- Python 3.x
- Flask 3.0.3
- Docker

## 설치 및 실행 방법

### 로컬 환경에서 실행

1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 서버 실행
```bash
python app.py
```

### Docker로 실행

1. Docker 이미지 빌드
```bash
docker build -t flask-backend .
```

2. Docker 컨테이너 실행
```bash
docker run -p 5000:5000 flask-backend
```

## API 엔드포인트

- `GET /`: 서버 상태 확인
- `GET /health`: 헬스 체크

## 환경 변수

- `FLASK_ENV`: 개발 환경 설정 (development/production)
- `PORT`: 서버 포트 (기본값: 5000)
