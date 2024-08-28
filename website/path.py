from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

path = Blueprint('path', __name__)


# 사용자 모델 정의 (UserMixin 포함)
class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def get_id(self):
        return self.email

# # 사용자 로드 함수 정의
# @login_manager.user_loader
# def load_user(email):
#     user_collection = db[email]
#     user_data = user_collection.find_one({"email": email})
#     if user_data:
#         return User(email=user_data['email'], password=user_data['password'])
#     return None

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.tgthon  


@path.route('/select', methods=["GET", "POST"])
@login_required  # 로그인한 사용자만 접근할 수 있게 제한
def select():
    user_collection = db[current_user.email]
    user_data = user_collection.find_one({"email": current_user.email})
    return render_template('select.html', user_data=user_data)

@path.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form['email']
        password = request.form['password']

    # Validation part
    # 사용자 컬렉션 확인
        existing_user = db.list_collection_names(filter={'name': email})
        if existing_user:
            flash('이미 존재하는 이메일입니다.', category='error')
            return redirect(url_for('path.sign_up'))

        # Create a document to insert inot MongoDB
        user = {
            'email': email,
            # 'password': generate_password_hash(password, method='sha256'),
            'password': password,
            'created_at': datetime.utcnow()
        }

        # Insert user data into MongoDB 
        # It's only user data, letters are other documents in each user collection

        # 사용자별 컬렉션 생성 후 데이터 삽입
        user_collection = db[email]
        user_collection.insert_one(user)

        # auto-login
        flash("회원가입 완료", category='success')
        return redirect(url_for('path.select')) # user page > select page

    return render_template('signup.html')



@path.route('/login/', methods=["GET", "POST"])
def login():
    # login
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # search User in database & compare password
        user_collection = db[email]
        user = user_collection.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            user_obj = User(email=user['email'], password=user['password'])
            login_user(user_obj, remember=True)  # 로그인 처리
            flash('로그인 완료', category='success')
            return redirect(url_for('path.select'))
        else:
            flash('잘못된 이메일 또는 비밀번호입니다.', category='error')
            return redirect(url_for('path.login'))

        # if user:
            # if check_password_hash(user.password, password1):
        # if user.find({'email': email}).get("password") == password:
            # flash('로그인 완료', category='success')
            # login_user(user, remember=True)
            # return redirect(url_for('select'))
        # else: 
        #     flash('비밀번호가 다릅니다.', category='error')
        # else:
        #     flash('해당 이메일 정보가 없습니다.', category='error')
    return render_template('main.html')

# log_out part

# @path.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('path.login'))


