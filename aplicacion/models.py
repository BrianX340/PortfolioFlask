from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean
from sqlalchemy import DateTime, Integer, String, Text, Float

from sqlalchemy.orm import relationship, backref
from aplicacion.main import db
from datetime import datetime


class Post(db.Model):
	"post"
	__tablename__ = "Post"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('facebloog_user.id', ondelete='SET NULL'))
	id_link = Column(String, nullable=False)
	fecha = Column(DateTime, default=datetime.now)
	texto = Column(String, nullable=False)

class User(db.Model):
	"User"
	__tablename__ = 'facebloog_user'
	#__table_args__ = {'extend_existing': True}
	id = Column(Integer, primary_key=True)

	name = Column(String, nullable=False)
	lastname = Column(String, nullable=False)

	email = Column(String, nullable=False)
	#phone = Column(String, nullable=False)
	password_hash = Column(String(128),nullable=False)

	#def __repr__(self):
	#    return f'<User {self.email}>'


	#def __repr__(self):
	#	return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

	def verify_password(self, password):
		if self.password_hash == password:
			return True
		else:
			return False

	def save(self):
		if not self.id:
			db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_by_id(id):
		return User.query.get(id)

	@staticmethod
	def get_by_email(email):
		return User.query.filter_by(email=email).first()


################################################################   FaceBloog  ################################################################



"""

class Wall(db.Model):
	"Muro"
	__tablename__ = "muro"
	id = Column(Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('facebloog_usuarios.id'),nullable=False)



class FacebloogPost(db.Model):
	"Publicaciones"
	__tablename__ = "publicacion"
	id = Column(Integer, primary_key=True)
	id_link = Column(String, nullable=False)
	titulo = Column(String, nullable=False)
	fecha = Column(DateTime, default=datetime.now)
	texto = Column(String, nullable=False)



class FacebloogUser(db.Model):
	"Usuarios"
	__tablename__ = 'facebloog_usuarios'
	id = Column(Integer, primary_key=True)

	wall = relationship("muro", lazy=True, backref='facebloog_usuarios')

	name = Column(String, nullable=False)
	lastname = Column(String, nullable=False)

	email = Column(String, nullable=False)
	phone = Column(String, nullable=False)
	password_hash = Column(String(128),nullable=False)


	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

	def verify_password(self, password):
		if self.password_hash == password:
			return True
		else:
			return False


class Person(db.Model):
	id = db.Column(Integer, primary_key=True)
	name = db.Column(String(50), nullable=False)
	wall = relationship('Wall', lazy='select',
		backref=db.backref('person', lazy='joined'))

class Wall(db.Model):
	id = Column(Integer, primary_key=True)
	email = Column(String(120), nullable=False)
	person_id = Column(Integer, ForeignKey('person.id'),
		nullable=False)
"""


"""
class FacebloogPost(db.Model):
	"Publicaciones"
	__tablename__ = "post"
	#__table_args__ = {'extend_existing': True}
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	image_name = Column(String)

	title = Column(String, nullable=False)
	created = Column(String, nullable=False) #default=datetime.now)
	content = Column(String, nullable=False)
	
	comments = db.relationship('FacebloogComments', backref='post', lazy=True, cascade='all, delete-orphan', order_by='asc(FacebloogComments.created)')

class FacebloogComments(db.Model):
	__tablename__ = "comments"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
	user_name = Column(String)
	post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
	created = Column(DateTime, default=datetime.utcnow)
	
	content = Column(Text)

	@staticmethod
	def get_by_post_id(post_id):
		return FacebloogComments.query.filter_by(post_id=post_id).all()
	
	@staticmethod
	def get_by_user_id(post_id):
		return FacebloogComments.query.filter_by(user_id=user_id).all()
	





#compmgmt para acceder a las cuentas de usuario



"""

		