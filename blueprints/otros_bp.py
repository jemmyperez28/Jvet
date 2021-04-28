from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from forms import  BuscarReservacion , NuevaReserva
from models import  Reservacion , Cliente
from sqlalchemy import exc , desc , func
otros_bp = Blueprint('otros_bp',__name__)

@otros_bp.route('/otros_reservacion', methods=['GET','POST'])
def otros_reservacion():
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    datos={}
    form_bus = BuscarReservacion()
    if request.method == "POST":
        fecha = form_bus.fecha.data 
        flag = 1
        datos = Reservacion.query.filter_by(idvet=idvet).filter_by(fecha=fecha).all()
        form_reserva = NuevaReserva()
        form_reserva.cargar_horas(idvet)
        form_reserva.buscar_empleado(idvet)
        return render_template("/app/reservaciones.html",datos=datos,form_bus=form_bus , flag=flag , fecha=fecha , form_reserva=form_reserva)   
    return render_template("/app/reservaciones.html",datos=datos,form_bus=form_bus)   

@otros_bp.route('/nueva_reserva', methods=['GET','POST'])
def nueva_reserva():
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    datos={}
    form_bus = NuevaReserva()
    if request.method == "POST":
        dni = form_bus.dni.data 
        fecha = form_bus.fecha.data 
        hora_inicio = form_bus.hora_inicio.data 
        encargado = form_bus.encargado.data 
        asunto = form_bus.asunto.data 
        existe = Cliente.query.filter_by(dni=dni).first()
        if existe is None:
            mensaje = 'Alerta ,El DNI/CE No esta Registrado ,  Debe Registrar al Cliente Primero'
            flash(mensaje)
            flag = 1
            datos = Reservacion.query.filter_by(idvet=idvet).filter_by(fecha=fecha).all()
            form_reserva = NuevaReserva()
            form_reserva.cargar_horas(idvet)
            form_reserva.buscar_empleado(idvet)
            return render_template("/app/reservaciones.html",datos=datos,form_bus=form_bus , flag=flag , fecha=fecha , form_reserva=form_reserva)
        try :            
            nuevo_reserva = Reservacion(idvet,dni,str(existe.nombre + ' ' + existe.apellidos), existe.telefono , existe.email,fecha,hora_inicio,None,asunto,encargado,"creado")
            db.session.add(nuevo_reserva)
            db.session.commit()
            mensaje='Se Creo La Reservacion RSV0' + str(nuevo_reserva.idreservacion)
            flash(mensaje)
            flag = 1
            datos = Reservacion.query.filter_by(idvet=idvet).filter_by(fecha=fecha).all()
            form_reserva = NuevaReserva()
            form_reserva.cargar_horas(idvet)
            form_reserva.buscar_empleado(idvet)
            return render_template("/app/reservaciones.html",datos=datos,form_bus=form_bus , flag=flag , fecha=fecha , form_reserva=form_reserva)
        except exc.SQLAlchemyError as e:
            mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
            flash(mensaje)
            return redirect(url_for('otros_bp.otros_reservacion'))
    return "Reinicie App PRDBP38"
