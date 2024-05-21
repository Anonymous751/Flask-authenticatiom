from Now_Flask import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(sno):
    return User.query.get(int(sno))



class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phn_no = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

class User(UserMixin, db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(12), nullable=False)
    image_file = db.Column(db.String(20), unique=False, default="default.jpg", nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

# this means(get_id) is mandaroty to get the user class id .....
    def get_id(self):
        return self.sno
    

    def get_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.sno}).decode('utf-8')
    
    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date_created}')"
    
class Blog_posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def get_data(self, title, desc, slug):
        return self.sno, self.title, self.desc, self.slug, self.date_created