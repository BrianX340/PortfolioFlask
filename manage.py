from flask_script import Manager
from aplicacion.main import app, db
from aplicacion.models import *

manager = Manager(app)
app.config['DEBUG'] = True # Ensure debugger will load.

@manager.command
def create_tables():
    "Create relational database tables."
    db.create_all()	

if __name__ == '__main__':
    manager.run()