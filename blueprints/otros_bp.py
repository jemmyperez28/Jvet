from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from forms import  BuscarReservacion , NuevaReserva , AtenderReservacion , EmpleadosForm
from models import  Reservacion , Cliente , Atencion , Cliente , Empleado
from sqlalchemy import exc , desc , func
from datetime import  datetime , timedelta , date
import pytz
import dateutil.parser
otros_bp = Blueprint('otros_bp',__name__)

@otros_bp.route('/eliminar_empleado', methods=['GET','POST'], defaults={'id':None})
@otros_bp.route('/eliminar_empleado/<int:id>', methods=['GET','POST'] )
def eliminar_empleado(id):
    idempleado = id 
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    form_em = EmpleadosForm()
    #Eliminar empleado 
    try :     
        Empleado.query.filter_by(idvet=idvet).filter_by(idempleado=idempleado).delete()
        db.session.commit()
        mensaje ="Eliminado Correctamente"
        flash(mensaje)
        datos = Empleado.query.filter_by(idvet=idvet).all()
        return render_template("/app/empleados.html",form_em=form_em,datos=datos)
    except exc.SQLAlchemyError as e:
        mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
        flash(mensaje)
        datos = Empleado.query.filter_by(idvet=idvet).all()
        return render_template("/app/empleados.html",form_em=form_em,datos=datos) 

@otros_bp.route('/empleados',methods=['GET','POST'])
def empleados():
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    form_em = EmpleadosForm()
    datos = Empleado.query.filter_by(idvet=idvet).all()
    if form_em.validate_on_submit():
        nombre = form_em.nombre.data 
        try:
            #(self,nombre,dni,password,atencion,petshop,reservaciones,servicios,productos,activo,idvet):
            nuevo_emp = Empleado(nombre,None,None,None,None,None,None,None,None,idvet)
            db.session.add(nuevo_emp)
            db.session.commit()
            mensaje = "Colaborador Creado "
            flash(mensaje)
            datos = Empleado.query.filter_by(idvet=idvet).all()
            return render_template("/app/empleados.html",form_em=form_em,datos=datos)   
        except exc.SQLAlchemyError as e:
            mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
            flash(mensaje)
            return render_template("/app/empleados.html",form_em=form_em,datos=datos)  
    return render_template("/app/empleados.html",form_em=form_em,datos=datos)   

@otros_bp.route('/crear_atencion', methods=['GET','POST'])
def crear_atencion():
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    form_res = AtenderReservacion()
    if request.method=="POST":
        idreservacion = form_res.idreservacion.data
        dni = form_res.dni.data
        nomape = form_res.nombre_apellido.data 
        email = form_res.email.data 
        atendido_por = form_res.atendido_por.data 
        mascota = form_res.mascota.data 
        sintomas = form_res.sintomas.data 
        informe = form_res.informe.data 
        receta = form_res.receta.data 
        observaciones = form_res.observaciones.data 
        try:
            nueva_atencion = Atencion(None,receta,sintomas,informe,observaciones,mascota,0.0,None,idvet,atendido_por,nombre_usuario,"abierto",nomape,dni,email,idreservacion)
            db.session.add(nueva_atencion)
            db.session.commit()
            mensaje = "Atencion Creada !"
            res = Reservacion.query.filter_by(idreservacion=idreservacion).first()
            res.estado_reservacion="atendido"
            db.session.commit()
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_atencion'))
        except exc.SQLAlchemyError as e:
            mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_atencion'))
    return "OBP47 App Error"

@otros_bp.route('/cancelar_reservacion', methods=['GET','POST'], defaults={'id':None})
@otros_bp.route('/cancelar_reservacion/<int:id>', methods=['GET','POST'] )
def cancelar_reservacion(id):
    idreservacion=id 
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    validar1 = Atencion.query.filter_by(idvet=idvet).filter_by(idreservacion=idreservacion).first()
    #Si Ya tiene atencion asociada. Mensaje No se puede Cancelar.
    if validar1 is not None:
        mensaje="Error , la Reserva ya Tiene una Atencion Asociada , No se Puede Cancelar"
        flash(mensaje)
        return redirect(url_for('otros_bp.otros_reservacion'))
    try:
        datos = Reservacion.query.filter_by(idreservacion=idreservacion).first()
        datos.estado_reservacion="cancelado"
        db.session.commit()
        mensaje="Se Cancelo la Reservacion RSV" + str(datos.idreservacion)
        flash(mensaje)
        return redirect(url_for('otros_bp.otros_reservacion'))
    except exc.SQLAlchemyError as e:
        mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
        flash(mensaje)
        return redirect(url_for('otros_bp.otros_reservacion'))
    return "108BPOTR CODE ERROR"

@otros_bp.route('/atender_reservacion', methods=['GET','POST'], defaults={'id':None})
@otros_bp.route('/atender_reservacion/<int:id>', methods=['GET','POST'] )
def atender_reservacion(id):
    idreservacion = id 
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    form_res = AtenderReservacion()
    #Validar si Reservacion pertenece a Veterinaria para atenderla.
    datos = Reservacion.query.filter_by(idvet=idvet).filter_by(idreservacion=idreservacion).first()
    if datos is None:
        mensaje = 'Ud No tiene los permisos suficientes para Atender esta reservacion'
        flash(mensaje)
        return redirect(url_for('otros_bp.otros_reservacion'))
    #Validar si Estado de Resrvacion  es cancelado 
    if datos.estado_reservacion=="cancelado":   
        mensaje = 'Error No se Puede Atender una Reserva Cancelada'
        flash(mensaje)
        return redirect(url_for('otros_bp.otros_reservacion')) 

    #Validar si Ya Existe una Atencion con El Codigo de Reservacion unico.
    existe = Atencion.query.filter_by(idvet=idvet).filter_by(idreservacion=datos.idreservacion).first()
    if existe is not None:
        mensaje = 'Atendiendo Reserva , Codigo de Atencion ATE' + str(existe.idatencion)
        flash(mensaje)
        return redirect(url_for('admin_bp.editar_atencion',id=existe.idatencion))
    #Buscar id del cliente a partir del dni
    cliente = Cliente.query.filter_by(dni=datos.dni).first()
    form_res.buscar_empleado(idvet)
    form_res.buscar_mascota(cliente.idcliente)
    return render_template("/app/atender_reservacion.html",datos=datos,form_res=form_res)   
    
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
        #Validar Fecha Ingresada >= Fecha HOY
        #obtener fecha hoy lima
        hoy = datetime.now(pytz.timezone('America/Lima')) # you could pass `timezone` object here
        hoy2 = dateutil.parser.parse(str(hoy)).date()
        if fecha < hoy2 :
            mensaje ='Alerta!, La Fecha De Reserva no puede ser menor a la de HOY'
            flash(mensaje)
            flag = 1
            datos = Reservacion.query.filter_by(idvet=idvet).filter_by(fecha=fecha).all()
            form_reserva = NuevaReserva()
            form_reserva.cargar_horas(idvet)
            form_reserva.buscar_empleado(idvet)
            return render_template("/app/reservaciones.html",datos=datos,form_bus=form_bus , flag=flag , fecha=fecha , form_reserva=form_reserva)

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
