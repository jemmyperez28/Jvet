from flask import Flask 
from config.db import db
from flask_migrate import Migrate
from blueprints.login_bp import login 
from blueprints.admin_bp import admin_bp
from blueprints.productos_bp import productos_bp
from blueprints.otros_bp import otros_bp
from blueprints.anon_bp import anon_bp

#Inicializacion de Variables 
app = Flask(__name__)
app.config.from_object('config.settings')
db.init_app(app)
migrate = Migrate(app, db)

#Registro de Blueprints
app.register_blueprint(login)
app.register_blueprint(admin_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(otros_bp)
app.register_blueprint(anon_bp)

#Para Desarrollo
if __name__ == '__main__':
    app.run(debug = True)

    