from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from models import Vet , Productos , Servicios , Empleado
from sqlalchemy import exc , desc , func
anon_bp = Blueprint('anon_bp',__name__)

@anon_bp.route('/', methods=['GET','POST'], defaults={'nom':None})
@anon_bp.route('/<nom>', methods=['GET','POST'] )
def index_anon(nom):
    nombre_vet = nom 
    if nombre_vet is None:
        datos = Vet.query.all()
        return render_template("/app/anon_index.html",datos=datos)
    else:
        datos = Vet.query.filter_by(nombre_unico=nombre_vet).first()
        productos = Productos.query.filter_by(idvet=datos.idvet).all()
        servicios = Servicios.query.filter_by(idvet=datos.idvet).all()
        empleados = Empleado.query.filter_by(idvet=datos.idvet).all()
        return render_template("/app/anon_vet.html",datos=datos , productos=productos,servicios=servicios,empleados=empleados)


