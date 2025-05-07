from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "docker 배포 테스트를 위한 임시서버"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
