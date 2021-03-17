from flask import Flask 
from config.db import db
from flask_migrate import Migrate
from blueprints.login_bp import login 
from blueprints.admin_bp import admin_bp


#Inicializacion de Variables 
app = Flask(__name__)
app.config.from_object('config.settings')
db.init_app(app)
migrate = Migrate(app, db)

#Registro de Rutas 
app.register_blueprint(login)
app.register_blueprint(admin_bp)

#Para Desarrollo
if __name__ == '__main__':
    app.run(debug = True)

    