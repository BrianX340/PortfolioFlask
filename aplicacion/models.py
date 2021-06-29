from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, DateTime, String, Text, Float
from sqlalchemy.orm import relationship, backref
from aplicacion.main import db
from datetime import datetime
import hashlib

################################################################   FaceBloog  ################################################################

class User(db.Model):
    """User"""
    __tablename__ = 'facebloog_user'
    email = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    #phone = Column(String, nullable=False)
    password = Column(String(128), nullable=False)
    profile_photo = Column(String, nullable=False)

    def setProfilePhoto(self, name_photo):
        self.profile_photo = name_photo

    def deleteProfilePhoto(self):
        self.profile_photo = 'none'

    def setEmail(self, email):
        email = [x.lower() for x in email]
        email = ''.join(email)
        self.email = email

    def setLastName(self, lastname):
        lastname = [x.lower() for x in lastname]
        lastname = ''.join(lastname)
        self.lastname = lastname

    def setName(self, name):
        name = [x.lower() for x in name]
        name = ''.join(name)
        self.name = name

    def setPassword(self, clave):
        clave = hashlib.new("sha1", clave.encode("utf-8"))
        self.password = clave.hexdigest()

    def __repr__(self):
        return f'<User {self.email}>'

    def verify_password(self, password):
        password = hashlib.new("sha1", password.encode("utf-8"))

        if self.password == password.hexdigest():
            return True
        else:
            return False

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Post(db.Model):
    """Post"""
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    email = Column(String, ForeignKey(
        'facebloog_user.email', ondelete='SET NULL'))
    fecha = Column(DateTime, default=datetime.now)
    texto = Column(String, nullable=False)

    def __repr__(self):
        return f'<Post by user_id: {self.email}>'

    def getContent(self):
        return self.texto

class Comments(db.Model):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    email_id = Column(String, ForeignKey(
        'facebloog_user.email', ondelete='SET NULL'))
    post_id = Column(String, ForeignKey('post.id', ondelete='SET NULL'))
    created = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)

    @staticmethod
    def get_by_post_id(post_id):
        return Comments.query.filter_by(post_id=post_id).all()

    @staticmethod
    def get_by_user_id(self):
        return Comments.query.filter_by(email_id=self.email_id).all()

    def __repr__(self):
        return f'<Comment by {self.email_id} in post {self.post_id}>'

    def getTime(self):
        return self.created.strftime('%m/%d/%Y')

    def getContent(self):
        return self.content
