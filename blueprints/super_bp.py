from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from models import HistorialSuscripcion, PagoSuscripcion, Suscripcion, Vet , Vendedor , Uservet , PagoVendedor , HistorialPagovendedor ,ttt as T 
from sqlalchemy import exc , desc , func
from forms import VendedorForm , ForgotPassword2 , LoginSuper , ModificarUsuario , ModificarVet , NuevoVendedorForm
from funciones import encriptar , super_required
from datetime import datetime
import datetime as dt 
import pytz
import dateutil.parser
from dateutil.relativedelta import relativedelta
super_vp = Blueprint('super_vp',__name__)


@super_vp.route('/super_depositovendedor/<id>', methods=['GET','POST'])
@super_required
def super_depositovendedor(id):
    idpagovendedor = id 
    #PagoVendedor
    pagovendedor = PagoVendedor.query.filter_by(idpagovendedor=idpagovendedor).first()
    pagovendedor.estado = "Pago Depositado"
    db.session.flush()
    #Historial de Pago al Vendedor
    nuevo_hpv = HistorialPagovendedor(None, pagovendedor.idvendedor, "Sistemas" , "Se Realizo un Deposito" , "El Codigo de Pago :" + str(pagovendedor.idpagovendedor) + " , Se Realizo el deposito correspondiente! ")
    db.session.add(nuevo_hpv)
    db.session.commit()
    mensaje = "Deposito OK"
    flash(mensaje)
    return redirect(url_for('super_vp.super_pagosv'))
@super_vp.route('/super_cancelarpago/<id>', methods=['GET','POST'])
@super_required
def super_cancelarpago(id):
    idpago = id
    #PagoSuscripcion
    pagosus = PagoSuscripcion.query.filter_by(idpagosuscripcion = idpago).first()
    pagosus.estado = "Operacio Cancelada"
    pagosus.observacion = "El Pago No Pudo Ser Verificado."
    db.session.flush()
    #HistorialSuscripcion
    nuevo_hs = HistorialSuscripcion(pagosus.idsuscripcion,None,"El pago No Pudo Ser Verificado Porfavor genere otro pago o consulte con Soporte el motivo" )
    db.session.add(nuevo_hs)
    db.session.flush()
    #Modifico Pago Vendedor
    pagovendedor = PagoVendedor.query.filter_by(idpagosuscripcion=idpago).first()
    pagovendedor.estado = "Operacion Cancelada"
    db.session.flush()
    #Historial de Cancelado
    nuevo_hpv = HistorialPagovendedor(None, pagovendedor.idvendedor, "Sistemas" , "Transaccion Cancelada" , "El Codigo de Pago :" + str(pagovendedor.idpagovendedor) + " Se Cancelo por sistemas. Indique al cliente que genere otro pago ")
    db.session.add(nuevo_hpv)
    db.session.commit()
    mensaje = "Pago Cancelado!"
    flash(mensaje)
    return redirect(url_for('super_vp.super_pagos'))

@super_vp.route('/super_validarpago/<id>', methods=['GET','POST'])
@super_required
def super_validarpago(id):
    idpago = id
    #PagoSuscripcion
    hoy = datetime.now(pytz.timezone('America/Lima'))
    pagosus = PagoSuscripcion.query.filter_by(idpagosuscripcion = idpago).first()
    pagosus.estado = "Pago OK!"
    pagosus.observacion = "Se Valido el Pago el Dia : " + str(hoy)
    db.session.flush()
    #Agrega 30 dias a Suscripcion.
    suscripcion = Suscripcion.query.filter_by(idsuscripcion=pagosus.idsuscripcion).first()
    suscripcion.tipo = "Pago"
    suscripcion.fecha_renovacion = suscripcion.fecha_renovacion + relativedelta(months=1)
    old_fecha_venc = suscripcion.fecha_vencimiento
    suscripcion.fecha_vencimiento = suscripcion.fecha_vencimiento + relativedelta(months=1)
    #HistorialSuscripcion.
    nuevo_hs = HistorialSuscripcion(pagosus.idsuscripcion,None,"Pago Validado : PAG" + str(idpago) ,"El Pago del mes de : " + str(pagosus.mes)+ str(pagosus.anio) +" Fue Validado Correctamente , 30 dias fueron agregados a la fecha de vencimiento : "  + str(old_fecha_venc) )
    db.session.add(nuevo_hs)
    db.session.flush()
    #Modifico Pago Vendedor
    pagovendedor = PagoVendedor.query.filter_by(idpagosuscripcion=idpago).first()
    pagovendedor.estado = "Pendiente Deposito"
    db.session.flush()
    #Se Agrega Historial Pago Vendedor.
    nuevo_hpv = HistorialPagovendedor(None, pagovendedor.idvendedor, "Sistemas" , "Deposito Pendiente" , "El Codigo de Pago :" + str(pagovendedor.idpagovendedor) + " Fue Validado , Esta Pendiente el Deposito al numero de cuenta proporcionado ")
    db.session.add(nuevo_hpv)
    db.session.commit()
    mensaje = "TODO OK!"
    flash(mensaje)
    return redirect(url_for('super_vp.super_pagos'))



@super_vp.route('/super_pagosv')
@super_required
def super_pagosv():
    pagosv = PagoVendedor.query.all() 
    hpagosv = HistorialPagovendedor.query.all()
    return render_template('/app/super_pagosv.html' , pagosv=pagosv, hpagosv=hpagosv)

@super_vp.route('/super_pagos')
@super_required
def super_pagos():
    #pagosv = PagoVendedor.query.all() 
    #hpagosv = HistorialPagovendedor.query.all()
    pagos = PagoSuscripcion.query.all()
    sus = Suscripcion.query.all()
    hsus = HistorialSuscripcion.query.all()
    return render_template('/app/super_pagos.html' , sus=sus, hsus=hsus , pagos= pagos)

@super_vp.route('/super_activarvend/<id>', methods=['GET','POST'])
@super_required
def super_activarvend(id):
    mensaje = ''
    idvend = id 
    dato = Vendedor.query.filter_by(idvendedor=idvend).first()
    dato.activo = "si"
    db.session.commit()
    mensaje = 'El Vendedor Fue Activado'
    flash(mensaje)
    return redirect(url_for('super_vp.super_vendedores'))

@super_vp.route('/super_vendedores', methods=['GET','POST'])
@super_required
def super_vendedores():
    datos = Vendedor.query.all()
    form_vendedor = NuevoVendedorForm()
    if request.method == "GET":
        return render_template("app/vendedores.html",form_vendedor=form_vendedor , datos=datos)
    if form_vendedor.validate_on_submit():
        dni = form_vendedor.dni.data
        correo = form_vendedor.correo.data
        password = form_vendedor.password.data
        npassword = encriptar(password)
        nombre = form_vendedor.nombre.data
        apellidos = form_vendedor.apellidos.data
        telefono = form_vendedor.telefono.data
        #def __init__(self,dni,email,password,nombre,apellidos,telefono,banco,nro_cuenta,nro_cuenta_int,activo):
        nuevo_vendedor = Vendedor(dni,correo,npassword,nombre,apellidos,telefono,None,None,None,"no")
        db.session.add(nuevo_vendedor)
        db.session.commit()
        mensaje = 'Se Agrego el Vendedor , Activelo Porfavor'
        flash(mensaje)
        return redirect(url_for('super_vp.super_vendedores'))




@super_vp.route('/super_modificavet', methods=['GET','POST'] , defaults={'id':None})
@super_vp.route('/super_modificavet/<int:id>', methods=['GET','POST'])
@super_required
def super_modificavet(id):
    idvet = id 
    form_vet = ModificarVet()
    if request.method == "GET":
        datos = Vet.query.filter_by(idvet=idvet).first()
        return render_template("/app/modificar_vet.html" , form_vet=form_vet,datos=datos)
    if form_vet.validate_on_submit():
        idvet = form_vet.id.data 
        mensaje = form_vet.mensaje.data  
        mision = form_vet.mision.data  
        vision = form_vet.vision.data   
        nombre_unico = form_vet.nombre_unico.data 
        clave_reporte = form_vet.clave_reporte.data 
        datos = Vet.query.filter_by(idvet=idvet).first() 
        datos.mensaje = mensaje 
        datos.mision = mision
        datos.vision = vision
        datos.nombre_unico = nombre_unico
        datos.clave_reporte = clave_reporte
        db.session.commit()
        mensaje = 'Actualizado'
        flash(mensaje)
        return redirect(url_for('super_vp.super_vets'))


@super_vp.route('/app/super_vets', methods=['GET','POST'])
@super_required
def super_vets():        
    datos = Vet.query.all()
    return render_template("/app/super_vets.html", datos=datos)


@super_vp.route('/ttt/<nom>', methods=['GET','POST'])
def ttt(nom):
    sec = nom 
    if sec == "revive_the_soul":
        log_vp = LoginSuper()
        return (render_template("/app/tttlog.html",log_vp=log_vp))

@super_vp.route('/ttt/log', methods=['POST'])
def log():
    if request.method == "POST":
        user = request.form["user"]
        pass1 = request.form["pass1"]
        pass2 = request.form["pass2"]
        data = T.query.first()
        if data.user == user:
            if data.pass1 == encriptar(pass1):
                if data.pass2 == encriptar(pass2):
                    session['loggedin'] = True 
                    session['tipo_uservet'] = 'super'
                    return redirect(url_for('super_vp.super_clientes'))
    return "404"

@super_vp.route('/app/super_clientes', methods=['GET','POST'])
@super_required
def super_clientes():        
    datos = Uservet.query.all()
    return render_template("/app/super_clientes.html", datos=datos)

@super_vp.route('/super_activaruser/<id>', methods=['GET','POST'])
@super_required
def super_activauser(id):
    mensaje = ''
    idusuario = id 
    dato = Uservet.query.filter_by(iduservet=idusuario).first()
    dato.validado = "si"
    db.session.commit()
    mensaje = 'El Usuario Fue Activado'
    flash(mensaje)
    return redirect(url_for('super_vp.super_clientes'))



@super_vp.route('/super_modificauser', methods=['GET','POST'] , defaults={'id':None})
@super_vp.route('/super_modificauser/<int:id>', methods=['GET','POST'])
@super_required
def super_modificauser(id):
    idusuario = id 
    form_user = ModificarUsuario()
    if request.method == "GET":
        datos = Uservet.query.filter_by(iduservet=idusuario).first()
        return render_template("/app/modificar_uservet.html" , form_user=form_user,datos=datos)
    if form_user.validate_on_submit():
        iduser = form_user.id.data 
        clave = form_user.clave.data
        validado = form_user.validado.data 
        datos = Uservet.query.filter_by(iduservet=iduser).first()
        datos.password = clave 
        datos.validado = validado 
        db.session.commit()
        mensaje = 'Actualizado'
        flash(mensaje)
        return redirect(url_for('super_vp.super_clientes'))





    
