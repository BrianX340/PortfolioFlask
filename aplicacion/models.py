from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from aplicacion.main import db
from datetime import datetime

class Publicacion(db.Model):
    """Publicaciones"""
    __tablename__ = "publicacion"
    id = Column(Integer, primary_key=True)
    id_link = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    texto = Column(String, nullable=False)

class User(db.Model):
	"""Usuarios"""
	__tablename__ = 'usuarios'
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False)
    #password = db.Column(db.String, nullable=False)
	password_hash = Column(String(128),nullable=False)
	name = Column(String, nullable=False)
	lastname = Column(String, nullable=False)
	#email = db.Column(db.String(200),nullable=False)
	#admin = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

	def verify_password(self, password):
		if self.password_hash == password:
			return True
		else:
			return False


    
class Muro(db.Model):
    """Muro"""
    __tablename__ = "muro"
    id = Column(Integer, primary_key=True)