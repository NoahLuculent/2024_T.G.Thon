from flask import Flask
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'semicircle_secret_key hollimoly guacamole roly poly' #

    
    # Flask-Login 설정
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'path.login'  # 로그인이 필요한 경우 리다이렉트할 뷰

    # 블루프린트 인스턴스 가져오기
    from .views import views
    from .path import path

    # 플라스크 앱에 등록하기
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(path, url_prefix='/')

  
    return app