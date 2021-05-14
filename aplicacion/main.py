from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

import hashlib

app = Flask(__name__)
app.config.from_object('aplicacion.config')
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)


################################################################   Comunicacion JS y Python  ################################################################


@app.route("/crear-facebloogpost", methods=["POST"])
def crear_facebloogpost():
	from aplicacion.models import User
	from aplicacion.models import Post
	from aplicacion.login import getEmailUser
	from aplicacion.login import is_login

	req = request.get_json()

	mensaje = str(req['message'])

	if is_login():
		email = getEmailUser()
		user = User.query.filter_by(email=email).first()
		texto = mensaje
		post = Post(texto=texto, email=user.email)
		db.session.add(post)
		db.session.commit()
		res = make_response(jsonify({"message": "OK"}), 200)
		return res

@app.route("/crear-facebloogcomments", methods=["POST"])
def crear_facebloogcomments():
	from aplicacion.models import User
	from aplicacion.models import Post
	from aplicacion.models import Comments
	from aplicacion.login import getEmailUser
	from aplicacion.login import is_login
	req = request.get_json()
	post_id = str(req['idpost'])
	texto = str(req['texto'])
	print(post_id,texto)

	if is_login():
		email = getEmailUser()
		user = User.query.filter_by(email=email).first()
		posts = Post.query.filter_by(id=post_id).first()
		comentario = Comments(content=texto, email_id=user.email, post_id=posts.id)
		db.session.add(comentario)
		db.session.commit()
		res = make_response(jsonify({"message": "OK"}), 200)
		return res



"""
@app.route("/facebloog")
def facebloog():
	from aplicacion.models import Post
	from aplicacion.models import Comments
	from aplicacion.login import getEmailUser
	from aplicacion.login import is_login
	

	if is_login():
		email = getEmailUser()
		posts = Post.query.filter_by(email=email).order_by(Post.fecha.desc()).all()
		comments = []
		for post in posts:
			comment = Comments.query.filter_by(post_id=post.id).order_by(Comments.created.desc()).all()
			if len(comment) > 0:
				comments.append(comment)
		print(comments)
		return render_template('facebloog-inicio.html', posts=posts,comments=comments,user=email)
	else:
		return render_template('facebloog-index.html')
"""

@app.route("/consulta-posteos", methods=["POST"])
def consulta_posteos():
	from aplicacion.models import Post
	from aplicacion.models import Comments
	from aplicacion.login import getEmailUser
	from aplicacion.login import is_login

	req = request.get_json()


	if is_login():
		email = getEmailUser()
		posts = Post.query.filter_by(email=email).order_by(Post.fecha.desc()).all()

		posteos = {}
		for post in posts:

			lista_comentarios = Comments.query.filter_by(post_id=post.id).order_by(Comments.created.desc()).all()
			comentarios = {}
			post_echo = {}	
			post_echo['useremail'] = post.email
			post_echo['postid'] = post.id
			post_echo['texto'] = post.texto

			if lista_comentarios != []:
				for comentario in lista_comentarios:
					comentarios[comentario.id] = {	'content':comentario.content,
													'user_comented':comentario.email_id,
													'coment_id':comentario.id
													}
			
			post_echo['coments'] = comentarios

			posteos[post.id] = post_echo

		bloqueEcho = ''
		bloqueEchoDerecho = []
		for post_echo in posteos:
			id_posteo = str(posteos[post_echo]['postid'])
			bloquePost = f"""
                        <div class='card'>
                            <div class='card-top'>
                                <h4>{ posteos[post_echo]['useremail'] }</h4>

                                <div class='delete-button' id='delete-button'method='post'>
                                <div value='{ id_posteo }' name='post_id'>X</div>
                                </div>
                            </div>
                            <div>
                                <p>{ posteos[post_echo]['texto'] }</p>
                            </div>
                            <div class='reactions'>
                            </div>
                    	"""

			bloqueComentarioCompleto = []
			for comentario in posteos[post_echo]['coments']:

				comentario_echo = f"""
				<div class='contenedorComentarios'>
					<div>
						<div>
							<span class='user'>{ posteos[post_echo]['coments'][comentario]['user_comented'] }</span>
							<span class='comentario'>{ posteos[post_echo]['coments'][comentario]['content'] }</span>
						</div>
					</div>
				</div>

				"""
				bloqueComentarioCompleto.append(comentario_echo)

			bloqueComentarioCompleto = bloqueComentarioCompleto[::-1]
			bloqueComentarioCompleto = ' '.join(bloqueComentarioCompleto)

			bloquePost += bloqueComentarioCompleto

			bloquePost += f"""
				<div class='contenedorTexto'>
					<div>
						<span class='span-text-input'>
							<span contenteditable='true' id='{ posteos[post_echo]['postid'] }' mensajetipo='comentario'
								class='comentarios_otros badge alert-info' data-placeholder='Escribe un comentario...'
								data-focused-advice='Escribe un comentario...'></span>
						</span>
					</div>
				</div>
				</div>
			"""
			
			bloqueEcho += bloquePost

		res = make_response(jsonify({'bloque': bloqueEcho}), 200)
		return res



################################################################   Principal  ################################################################

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


################################################################   FaceBloog  ################################################################

@app.route("/facebloog")
def facebloog():
	from aplicacion.models import Post
	from aplicacion.models import Comments
	from aplicacion.login import getEmailUser
	from aplicacion.login import is_login
	

	if is_login():
		email = getEmailUser()
		posts = Post.query.filter_by(email=email).order_by(Post.fecha.desc()).all()
		comments = []
		for post in posts:
			comment = Comments.query.filter_by(post_id=post.id).order_by(Comments.created.desc()).all()
			if len(comment) > 0:
				comments.append(comment)
		print(comments)
		return render_template('facebloog-inicio.html', posts=posts,comments=comments,user=email)
	else:
		return render_template('facebloog-index.html')

@app.route("/facebloog-perfil")
def facebloog_perfil():
	from aplicacion.login import getEmailUser
	from aplicacion.models import User

	user = getEmailUser()
	if user:
		user = User.query.get(user)
		return render_template('facebloog-profile.html', email = user.email, name=user.name,lastname=user.lastname)
	else:
		return redirect('facebloog')

@app.route("/facebloog", methods=["POST"])
def registrar_usuario_facebloog():
	from aplicacion.models import User

	nombre = request.form.get("name")
	apellido = request.form.get("lastname")
	email = request.form.get("emailregister")
	clave = request.form.get("passwordregister")
	user_email = User.query.filter_by(email=email).first()
	
	if user_email is not None:
		return render_template('facebloog-mensaje.html', email=email)
	else:
		userProfile = User(name=nombre, lastname=apellido, email=email)
		userProfile.setPassword(clave)
		db.session.add(userProfile)
		db.session.commit()


		return render_template('facebloog-index.html',email=email)

@app.route("/verificar-usuario", methods=["GET", "POST"])
def verificar_usuario_facebloog():
	from aplicacion.models import User
	from aplicacion.login import login_user
	from aplicacion.forms import LoginForm

	form = LoginForm()
	email = request.form.get("email_login")
	clave = request.form.get("password_login")
	user = User.query.filter_by(email=email).first()
	correcto = user.verify_password(clave)
	if correcto:
		login_user(user)
		return redirect('facebloog')
	return render_template('facebloog-loginfailed.html', email=email)




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