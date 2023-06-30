from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for
from flask_login import login_user, current_user, logout_user
from datetime import timedelta
from blog_control.user_mgmt import User

blog_abtest = Blueprint('blog_abtest', __name__)

@blog_abtest.route('/set_email', methods=['GET', 'POST'])
def set_email(): 
    print('set_email', request.headers)
    if request.method == 'GET':
        # get 은 content-type 이 헤더에 없음
        print('set_email', request.args.get('user_email'))
    else:
        # content_type 이 application/json 인 경우는 request.get_json() 을 통해 파라미터 값 얻을 수 있음
        # x-www-form 인 경우 request.form 을 써야함 주로 html 에서 post 로 호출할떼 form인 경우가 많음
        print('set_email', request.form['user_email'])
        user = User.create(request.form['user_email'], 'A')
        login_user(user, remember=True, duration=timedelta(days=31)) # 사용자 request 의 header (사용자의 ip)와 user 객체의 id, 서버의 secret_key 를 기반으로 session 을 만듦. session 은 flask_login 만의 기능이 아닌 flask 자체의 기능임.
        
    # return make_response(jsonify(success = True), 200)
    return redirect(url_for('blog_abtest.test_blog')) 
    # redirect 는 라우팅 경로를 다르게 해서 리턴함 (ex. get 방식인 경우 응답할때 설정한 라우팅 경로로 초기화.) url_for은 redirect('/blog/test_blog')와 동일한 역할
  
    # redirect 는 라우팅 경로를 다르게 해서 리턴함 (ex. get 방식인 경우 응답할때 설정한 라우팅 경로로 초기화.) url_for은 redirect('/blog/test_blog')와 동일한 역할

@blog_abtest.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog_abtest.test_blog')) 
    
@blog_abtest.route('/test_blog')
def test_blog():
    # Flask 에서는 세션을 user_id 별로 관리
    if current_user.is_authenticated: # 내부적으로 blog_abtest 의 load_user(user_id) 함수를 호출해서 인증된 사용자인지 확인함. current_user 객체는 User.get() 으로 반환된 User 의 모든 속성을 가짐. user_id 는 사용자의 http request 에서 추출함.
        return render_template('blog_A.html', user_email=current_user.user_email) # render_template 은 jinja2 라이브러리로 html 의 user_email 의 값을 대입 후 클라이언트에 그 html 을 전송
    else:
        return render_template('blog_A.html')