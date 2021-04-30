from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from aplicacion.forms import LoginForm


app = Flask(__name__)
app.config.from_object('aplicacion.config')
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)

"""
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)
    texto = db.Column(db.String, nullable=False)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
"""


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/html-css")
def html_css():
    return render_template('1-HTML-CSS.html')

#@app.route("/photoshop")
#def photoshop():
#    return render_template('3-photoshop.html')

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

@app.route("/logout")
def logout():
    from aplicacion.login import logout_user
    logout_user()
    return redirect('blog-login')

@app.route("/blog-login")
def blog_login():
    return render_template('blog-login.html')

@app.route("/login_verify", methods=["GET", "POST"])
def login_verify():
    from aplicacion.models import User
    from aplicacion.login import login_user
    import hashlib

    form = LoginForm()

    usuario = request.form.get("user")
    clave = request.form.get("password")
    clave_hash = hashlib.new("sha1", clave.encode("utf-8"))

    user = User.query.filter_by(username=usuario).first()

    if user.password_hash == clave_hash.hexdigest():
        login_user(user)
        return redirect('blog-loged')
    
    return render_template('blog-login.html', form=form)


@app.route("/register")
def blog_register():
    return render_template('blog-register.html')

@app.route("/user-register", methods=["POST"])
def registrar_usuario():
    import hashlib
    from aplicacion.models import User

    nombre = request.form.get("name")
    apellido = request.form.get("last_name")
    usuario = request.form.get("user")
    clave = request.form.get("password")
    clave_hash = hashlib.new("sha1", clave.encode("utf-8"))
    userProfile = User(name=nombre, lastname=apellido, username=usuario, password_hash=clave_hash.hexdigest())
    db.session.add(userProfile)
    db.session.commit()
    return redirect("/blog-login")

@app.route("/blog-loged")
def blog_loged():
    from aplicacion.models import Publicacion
    from aplicacion.login import getUserName
    posts = Publicacion.query.filter_by(id_link=getUserName()).order_by(Publicacion.fecha.desc()).all() # select * from post order by time
    print(posts)
    return render_template('blog-loged.html', posts=posts)

"""
@app.route("/blog")
def blog():
    return render_template('blog-inicio.html')

@app.route("/blog-post")
def blog_post():
    from aplicacion.models import Publicacion
    posts = Publicacion.query.order_by(Publicacion.fecha.desc()).all() # select * from post order by time
    return render_template('blog-inicio.html', posts=posts)

"""

@app.route("/blog-agregar")
def blog_agregar():
    return render_template("blog-agregar.html")

@app.route("/crear-post", methods=["POST"])
def crear_post():
    from aplicacion.models import Publicacion
    from aplicacion.login import is_login
    from aplicacion.login import getUserName
    print(getUserName())
    if is_login():
        id_user = getUserName()
        titulo = request.form.get("titulo")
        texto = request.form.get("texto")
    post = Publicacion(id_link=id_user,titulo=titulo, texto=texto)
    db.session.add(post)
    db.session.commit()
    return redirect("/blog-loged")

@app.route("/borrar", methods=["POST"])
def borrar_post():
    from aplicacion.models import Publicacion
    post_id = request.form.get("post_id")
    post = db.session.query(Publicacion).filter(Publicacion.id==post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('blog-loged')
    
"""
#app.run(debug=True,host='192.168.0.5', port=5000,threaded=True)
app.run(debug=True,host='192.168.0.5', port=5000,threaded=True)
"""