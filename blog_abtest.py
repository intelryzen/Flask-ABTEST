from flask import Flask, jsonify, request, render_template, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from blog_view import blog
from blog_control.user_mgmt import User
import os

# https 만을 지원하는 기능을 http 에서 테스트할 때 필요한 설정
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'

app = Flask(__name__, static_url_path='/static') # html 파일 내 필요한 소스는 static에서 가져옴.
CORS(app) # 여기서는 사실 필요없음.
app.secret_key = 'server Key'

app.register_blueprint(blog.blog_abtest, url_prefix='/blog')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler # 로그인하지 않은 사용자가 비인가(로그인 필요)된 api를 호출하면
def unauthorized():
    return make_response(jsonify(success = False), 401)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)