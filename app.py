from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 16바이트 길이의 무작위 키 생성

# MongoDB 클라이언트 설정 (로컬 MongoDB에 연결)
client = MongoClient('mongodb://localhost:27017/')
db = client['Timeletter']  # 데이터베이스 이름 설정
users_collection = db['userdata']  # 사용자 데이터를 저장할 컬렉션 설정

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def create_account():
    return render_template('create.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    password_check = request.form['password-check']
    phone = request.form['phone']

    # 비밀번호 확인
    if password != password_check:
        return jsonify({"error": "Passwords do not match"}), 400

    # 이메일 중복 확인
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 400

    # 비밀번호 해시 처리
    hashed_password = generate_password_hash(password)
    user_data = {
        "email": email,
        "password": hashed_password,
        "phone": phone
    }
    users_collection.insert_one(user_data)

    return redirect(url_for('home'))  # 가입 후 로그인 페이지로 리디렉션

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = users_collection.find_one({"email": email})
    print(f"User found: {user}")  # 사용자 정보 출력

    if user and check_password_hash(user['password'], password):
        session['user_id'] = str(user['_id'])
        session['email'] = user['email']
        print(f"Login successful: {session}")  # 세션 정보 출력
        return redirect(url_for('select'))
    else:
        print("Login failed: Invalid email or password")  # 실패 로그
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/select')
def select():
    if 'user_id' in session:
        return render_template('select.html', user_email=session['email'])
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
@app.route('/write')
def write_letter():
    if 'user_id' in session:
        return render_template('write.html')
    else:
        return redirect(url_for('home'))

@app.route('/view')
def view_letter():
    if 'user_id' in session:
        return render_template('view.html')
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


