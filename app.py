from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from bson import ObjectId

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
        session['phone'] = user['phone']
        print(f"Login successful: {session}")  # 세션 정보 출력
        return redirect(url_for('select'))
    else:
        print("Login failed: Invalid email or password")  # 실패 로그
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/kakao', methods=["GET"])
def kakao():

        #번호 있으면 :
        #카톡 로그인 이력? session[]
        return redirect(url_for('select'))
    #else:
     #   return render_template('phonenum.html')

@app.route('/kakao/register', methods=['POST'])
def kakao_phone():
    phone = request.form['phone']
    user_data = {
        'phone': phone
    }
    users_collection.insert_one(user_data)
    session['phone'] = phone
    return redirect(url_for('select'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# MongoDB에 데이터 추가 스크립트 (임의로 3개의 데이터 추가)
client = MongoClient('mongodb://localhost:27017/')
db = client['Timeletter']
letters_collection = db['letters']




@app.route('/select')
def select():
    if 'user_id' in session:
        return render_template('select.html', user_email=session['email'])
    else:
        return redirect(url_for('home'))
    
@app.route('/select')
def select_page():
    return render_template('select.html')


@app.route('/write')
def write_letter():
    if 'user_id' in session:
        return render_template('write.html')
    else:
        return redirect(url_for('home'))

# 편지 보기 페이지
@app.route('/letter/<letter_id>')
def letter_page(letter_id):
    
    # MongoDB에서 편지 데이터 가져오기
    try:
        letter = letters_collection.find_one({"_id": ObjectId(letter_id)})
        if letter:
            return jsonify({
                'title': letter.get('letter_title'),
                'sender': letter.get('sender_name'),
                'sent_date': letter.get('sent_at'),
                'received_date': letter.get('received_date'),
                'content': letter.get('content')
            })
        else:
            return jsonify({'error': '편지를 찾을 수 없습니다.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/submit_letter', methods=['POST'])
def submit_letter():
    year = request.form['year'],
    month = request.form['month'],
    day = request.form['day'],
    fixed = request.form.get('fixed'),
    sender_name = request.form['sender-name'],
    sender_phone = request.form['sender-phone'],
    receiver_name = request.form['receiver-name'],
    receiver_phone = request.form['receiver-phone'],
    letter_title = request.form['letter-title'],
    anonymous = 'anonymous' in request.form
    notepad = request.form['notepad']
    
    # 여기에서 받은 데이터를 데이터베이스에 저장하거나 처리합니다.
    letter = {
    'year': year,
    'month': month,
    'day': day,
    'fixed': fixed,
    'sender_name': sender_name,
    'sender_phone': sender_phone,
    'receiver_name': receiver_name,
    'receiver_phone': receiver_phone,
    'letter_title': letter_title,
    'anonymous': 'anonymous' in request.form,
    'notepad': notepad,
    'sent_at': datetime.utcnow()
    }
    letters_collection.insert_one(letter)
    # 이후, 성공 시 select.html로 리다이렉트합니다.
    return redirect(url_for('done'))


@app.route('/view')
def view_letter():
    if 'user_id' in session:
        phone = session['phone']
        letters = letters_collection.find({"receiver_phone": phone})
        return render_template('view.html', letters=letters)
    else:
        return redirect(url_for('home'))
        

@app.route('/done')
def done():
    return render_template('done.html')

if __name__ == '__main__':
    app.run(debug=True)




