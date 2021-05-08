from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from aplicacion.forms import LoginForm
import hashlib



app = Flask(__name__)
app.config.from_object('aplicacion.config')
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)



@app.route("/")
def index():
	return render_template('index.html')

@app.route("/html-css")
def html_css():
	return render_template('1-HTML-CSS.html')

@app.route("/contact")
def contact():
	return render_template('contact.html')

@app.route("/habilidades")
def habilidades():
	return render_template('4-habilidades.html')

@app.route("/cursos")
def cursos():
	return render_template('5-cursos.html')

@app.route("/acerca-de-mi")
def acerca_de_mi():
	return render_template('6-acerca-de-mi.html')

@app.route("/cv")
def cv():
	return render_template('7-cv-pdf.html')


"""
#app.run(debug=True,host='192.168.0.5', port=5000,threaded=True)
app.run(debug=True,host='192.168.0.5', port=5000,threaded=True)
"""


################################################################   FaceBloog  ################################################################


@app.route("/facebloog")
def facebloog():
	from aplicacion.login import is_login
	from aplicacion.models import Post
	from aplicacion.login import getUserName
	
	if is_login():
		posts = Post.query.filter_by(id_link=getUserName()).order_by(Post.fecha.desc()).all() # select * from post order by time
		return render_template('facebloog-inicio.html', posts=posts)
	else:
		return render_template('facebloog-index.html')

@app.route("/facebloog-perfil")
def facebloog_perfil():
	from aplicacion.models import User
	from aplicacion.login import getUserName
	email = getUserName()
	if getUserName():
		user_email = getUserName()
		user = db.session.query(User).filter(User.email==user_email).first()
		return render_template('facebloog-profile.html', email = user.email, name=user.name,lastname=user.lastname)
	else:
		return redirect('facebloog')

@app.route("/registrar-usuario-facebloog", methods=["POST"])
def registrar_usuario_facebloog():
	from aplicacion.models import User

	nombre = request.form.get("name")
	apellido = request.form.get("lastname")
	email = request.form.get("emailregister")
	clave = request.form.get("passwordregister")
	clave_hash = hashlib.new("sha1", clave.encode("utf-8"))

	print(nombre,apellido,email,clave)

	user_email = User.get_by_email(email)
	if user_email is not None:
		return render_template('facebloog-mensaje.html', email=email)
	else:
		userProfile = User(name=nombre, lastname=apellido, email=email, password_hash=clave_hash.hexdigest())
		db.session.add(userProfile)
		db.session.commit()
		return render_template('facebloog-registroexitoso.html', email=email)

@app.route("/verificar-usuario", methods=["GET", "POST"])
def verificar_usuario_facebloog():
	from aplicacion.models import User
	from aplicacion.login import login_user
	import hashlib

	form = LoginForm()

	email = request.form.get("email_login")
	clave = request.form.get("password_login")
	clave_hash = hashlib.new("sha1", clave.encode("utf-8"))

	user = User.query.filter_by(email=email).first()

	if user.password_hash == clave_hash.hexdigest():
		login_user(user)
		return redirect('facebloog')
	
	return render_template('facebloog-loginfailed.html', email=email)




@app.route("/crear-facebloogpost", methods=["POST"])
def crear_facebloogpost():
	from aplicacion.models import Post
	from aplicacion.login import is_login
	from aplicacion.login import getUserName

	if is_login():
		id_user = getUserName()
		texto = request.form.get("texto")
		post = Post(id_link=id_user, texto=texto)
		db.session.add(post)
		db.session.commit()
		return redirect("/facebloog")

@app.route("/borrar-facebloogpost", methods=["POST"])
def borrar_facebloogpost():
	from aplicacion.models import Post
	post_id = request.form.get("post_id")
	post = db.session.query(Post).filter(Post.id==post_id).first()
	db.session.delete(post)
	db.session.commit()
	return redirect('/facebloog')


@app.route("/facebloog-logout")
def facebloog_logout():
	from aplicacion.login import logout_user
	logout_user()
	return redirect('/facebloog')