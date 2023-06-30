from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for
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
    # return make_response(jsonify(success = True), 200)
    return redirect(url_for('blog_abtest.test_blog')) 
    # redirect 는 라우팅 경로를 다르게 해서 리턴함 (ex. get 방식인 경우 응답할때 설정한 라우팅 경로로 초기화.) url_for은 redirect('/blog/test_blog')와 동일한 역할
  

@blog_abtest.route('/test_blog')
def test_blog():
    return render_template('blog_A.html')