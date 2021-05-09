from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, DateTime, String, Text, Float
from sqlalchemy.orm import relationship, backref
from aplicacion.main import db
from datetime import datetime
import hashlib



################################################################   FaceBloog  ################################################################

class Post(db.Model):
	"""Post"""
	__tablename__ = "post"
	id = Column(Integer, primary_key=True)
	email = Column(String, ForeignKey('facebloog_user.email', ondelete='SET NULL'))
	fecha = Column(DateTime, default=datetime.now)
	texto = Column(String, nullable=False)

	def __repr__(self):
	    return f'<Post by user_id: {self.email}>'



class User(db.Model):
	"""User"""
	__tablename__ = 'facebloog_user'
	email = Column(String, primary_key=True, nullable=False)
	name = Column(String, nullable=False)
	lastname = Column(String, nullable=False)
	#phone = Column(String, nullable=False)
	password = Column(String(128),nullable=False)
	
	def setPassword(self,clave):
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


class Comments(db.Model):
	__tablename__ = "comments"
	id = Column(Integer, primary_key=True)
	email_id = Column(String, ForeignKey('facebloog_user.email', ondelete='SET NULL'))
	post_id = Column(String, ForeignKey('post.id', ondelete='SET NULL'))
	created = Column(DateTime, default=datetime.utcnow)
	content = Column(Text)

	@staticmethod
	def get_by_post_id(post_id):
		return Comments.query.filter_by(post_id=post_id).all()
	
	@staticmethod
	def get_by_user_id(post_id):
		return Comments.query.filter_by(email_id=email_id).all()

	def __repr__(self):
	    return f'<Comment by {self.email_id} in post {self.post_id}>'

	"""
	@staticmethod
	def get_by_id(id):
		return User.query.get(id)

	@staticmethod
	def get_by_email(email):
		return User.query.filter_by(email=email).first()
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


	
#compmgmt para acceder a las cuentas de usuario



"""

		