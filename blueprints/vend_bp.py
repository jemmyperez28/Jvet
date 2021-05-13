from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from models import Vet , Vendedor
from sqlalchemy import exc , desc , func
vend_bp = Blueprint('vend_bp',__name__)

@vend_bp.route('/index_vend', methods=['GET','POST'])
def index_vend():
    idvendedor = session['idvendedor'] 
    nombre = session['nombre'] 
    tipo = session['tipo_uservet'] 
    datos = Vendedor.query.filter_by(idvendedor=idvendedor).first()
    return render_template("/app/vend_index.html",datos=datos)







