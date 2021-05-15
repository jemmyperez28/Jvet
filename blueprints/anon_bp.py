from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from models import Vet , Productos , Servicios , Empleado
from sqlalchemy import exc , desc , func
anon_bp = Blueprint('anon_bp',__name__)

@anon_bp.route('/', methods=['GET','POST'])
def index_anon():
    datos = Vet.query.all()
    return render_template("/app/anon_index.html",datos=datos)


@anon_bp.route('/<nombre>',methods=['GET','POST'])
def vet(nombre):
    nombre_vet = nombre
    datos = Vet.query.filter_by(nombre_unico=nombre_vet).first()
    productos = Productos.query.filter_by(idvet=datos.idvet).all()
    servicios = Servicios.query.filter_by(idvet=datos.idvet).all()
    empleados = Empleado.query.filter_by(idvet=datos.idvet).all()   
    return render_template("/app/anon_vet.html",datos=datos , productos=productos,servicios=servicios,empleados=empleados)





