from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from models import Suscripcion, Vet , Vendedor , Uservet , PagoVendedor , HistorialPagovendedor
from sqlalchemy import exc , desc , func
from forms import VendedorForm , ForgotPassword2
from funciones import encriptar
vend_bp = Blueprint('vend_bp',__name__)

@vend_bp.route('/index_vend', methods=['GET','POST'])
def index_vend():
    idvendedor = session['idvendedor']
    nombre = session['nombre']
    tipo = session['tipo_uservet']
    form_vendedor = VendedorForm()
    datos = Vendedor.query.filter_by(idvendedor=idvendedor).first()
    if request.method == "GET":
        return render_template("/app/vend_index.html",datos=datos, form_vendedor = form_vendedor )
    if form_vendedor.validate_on_submit():
        nombre = form_vendedor.nombre.data
        apellidos = form_vendedor.apellidos.data
        telefono = form_vendedor.telefono.data
        banco = form_vendedor.banco.data 
        nro_cuenta  = form_vendedor.nro_cuenta.data 
        nro_cuenta_int  = form_vendedor.nro_cuenta_int.data 
        datos.nombre = nombre
        datos.apellidos = apellidos
        datos.telefono = telefono
        datos.banco = banco 
        datos.nro_cuenta = nro_cuenta 
        datos.nro_cuenta_int = nro_cuenta_int
        db.session.commit()
        mensaje = "Datos Actualizados Correctamente"
        flash(mensaje)
        return redirect(url_for('vend_bp.index_vend'))  

@vend_bp.route('/vend_clientes', methods=['GET','POST'])
def vend_clientes():
    idvendedor = session['idvendedor']
    nombre = session['nombre']
    tipo = session['tipo_uservet']
    #atenciones = .join(Cliente, Atencion.idcliente==Cliente.idcliente).add_columns(Cliente.nombre , Cliente.apellidos).order_by(Atencion.fecha_atencion.desc()).limit(5).all()
    datos = Uservet.query.with_entities(Uservet.email,Uservet.nombre,Uservet.apellidos,Uservet.telefono).join(Suscripcion, Uservet.idsuscripcion == Suscripcion.idsuscripcion).add_columns(Suscripcion.fecha_renovacion,Suscripcion.fecha_vencimiento,Suscripcion.estado,Suscripcion.idsuscripcion).all()
    print(datos)
    return render_template("/app/vend_clientes.html" ,datos=datos)


@vend_bp.route('/vend_pagos', methods=['GET','POST'])
def vend_pagos():
    idvendedor = session['idvendedor']
    nombre = session['nombre']
    tipo = session['tipo_uservet']
    pagos = PagoVendedor.query.filter_by(idvendedor=idvendedor).order_by(PagoVendedor.idvendedor.desc()).limit(20).all()
    hpagos = HistorialPagovendedor.query.filter_by(idvendedor=idvendedor).order_by(HistorialPagovendedor.creado.desc()).limit(20).all()
    return render_template("/app/vend_pagos.html" ,pagos=pagos, hpagos=hpagos)
