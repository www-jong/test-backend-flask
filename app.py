from flask import Flask, jsonify
import os
import pymysql
from pymysql import Error

app = Flask(__name__)


# 환경 변수에서 설정 가져오기
PORT = int(os.getenv('PORT', 5000))
USE_DB = os.getenv('USE_DB', 'true').lower() == 'true'
app_env=os.getenv('APP_ENV', 'unknown')
# 데이터베이스 설정 (USE_DB가 true일 때만 사용)
if USE_DB:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'test_db')

def get_db_connection():
    if not USE_DB:
        return None
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Error as e:
        print(f"MySQL 연결 에러: {e}")
        return None

@app.route('/')
def index():
    return jsonify({
        "status": "running",
        "message": "Flask server is running",
        "database_enabled": USE_DB
    })

@app.route('/health')
def health():
    if not USE_DB:
        return jsonify({
            "status": "healthy",
            "database": "disabled",
            "port": PORT,
            "env": app_env,
            "test":"Test",
            "test2":"Test7"
        })
    
    db_status = "connected" if get_db_connection() else "disconnected"
    return jsonify({
        "status": "healthy",
        "database": db_status,
        "env": app_env,
        "test":"Test",
        "test5":"Test5"
    })

@app.route('/db-test')
def db_test():
    if not USE_DB:
        return jsonify({
            "status": "error",
            "message": "Database is disabled"
        }), 400

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION() as version")
                version = cursor.fetchone()
            conn.close()
            return jsonify({
                "status": "success",
                "mysql_version": version['version']
            })
        except Error as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    return jsonify({
        "status": "error",
        "message": "Database connection failed"
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
