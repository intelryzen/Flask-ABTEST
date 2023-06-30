from db_model.mongodb import conn_mongodb
from datetime import datetime

class BlogSession(): # 여기서의 세션은 로그인에서의 세션/쿠키의 의미가 아닌 서비스의 세션을 의미함
    blog_page = {'A': 'blog_A.html', 'B': 'blog_B.html'}
    session_count = 0
    
    @staticmethod
    def save_session_info(session_ip, user_email, webpage_name):
        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        
        mongo_db = conn_mongodb()
        mongo_db.insert_one({
                'session_ip':session_ip,
                'user_email':user_email,
                'page':webpage_name,
                'access_time':now_time
            })
        
    @staticmethod
    def get_blog_page(blog_id=None):
        if blog_id == None:
            if BlogSession.session_count == 0:
                BlogSession.session_count = 1
                return BlogSession.blog_page['A']
            else:
                BlogSession.session_count = 0
                return BlogSession.blog_page['B']
        else:
            return BlogSession.blog_page[blog_id]
                