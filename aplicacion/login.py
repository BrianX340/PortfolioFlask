from flask import session, redirect

def login_user(Usuario):
    session["email"]=Usuario.email

def logout_user():
    session.pop("email",None)

def is_login():
	if "email" in session:
		return True
	else:
		return False	

def is_admin():
	return session.get("admin",False) 

def getEmailUser():
	if "email" in session:
		return session["email"]
	else:
		return False