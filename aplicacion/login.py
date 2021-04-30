from flask import session, redirect

def login_user(Usuario):
    session["id"]=Usuario.id
    session["username"]=Usuario.username

def logout_user():
    session.pop("id",None)
    session.pop("username",None)

def is_login():
	if "id" in session:
		return True
	else:
		return False	

def is_admin():
	return session.get("admin",False) 

def getUserName():
	if "id" in session:
		return session["username"]
	else:
		return False