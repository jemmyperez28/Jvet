from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from forms import AdminInfo , ForgotPassword , Veterinaria , VeterinariaFoto , ClienteForm , MascotaForm , BuscarCM , MascotaFormUpd , AtencionForm , AtencionDNI
from models import Uservet , Vet , Cliente , Mascota , Atencion , AtencionDetalle , Empleado
from funciones import encriptar
from config.db import db 
import os
from werkzeug.utils import secure_filename
#from config.settings import UPLOAD_FOLDER
#from config.keys import UPLOAD_FOLDER
import imghdr
from config.keys import extensiones
from sqlalchemy import exc , desc
import datetime

admin_bp = Blueprint('admin_bp',__name__)

@admin_bp.route('/index_admin', methods=['GET','POST'])
def index_admin():
    return render_template("/app/admin_index.html")     

@admin_bp.route('/admin_info', methods=['GET','POST'])
def admin_info():
    mensaje = ''
    form_admin_info = AdminInfo()
    form_forgot_password = ForgotPassword()
    iduservet = session['iduservet']
    if request.method == 'GET':
        datos = Uservet.query.filter_by(iduservet=iduservet).first()
        return render_template("/app/admin_info.html",form_admin_info=form_admin_info,datos=datos,form_forgot_password=form_forgot_password)
    #Form Informacion Personal
    if form_admin_info.validate_on_submit():
        nombre = form_admin_info.nombre.data
        apellidos = form_admin_info.apellidos.data
        telefono = form_admin_info.telefono.data
        usuario = Uservet.query.filter_by(iduservet=iduservet).first()
        usuario.nombre = nombre
        usuario.apellidos = apellidos
        usuario.telefono = telefono
        mensaje = "Datos Actualizados Correctamente"
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('admin_bp.admin_info'))
    #Form Actualizar Contraseña
    if form_forgot_password.validate_on_submit():
        password_old = form_forgot_password.password_old
        password1 = form_forgot_password.password1
        password2 = form_forgot_password.password2
        old_password = Uservet.query.with_entities(Uservet.password).filter_by(iduservet=iduservet).first()
        dato_antiguo = password_old.data
        dato_antiguo_encriptado = encriptar(dato_antiguo)
        nuevo_pass = password1.data 
        nuevo_pass_encrip = encriptar(nuevo_pass)
        if dato_antiguo_encriptado == old_password.password:
            if password1.data == password2.data:
                usuario = Uservet.query.filter_by(iduservet=iduservet).first()
                usuario.password = nuevo_pass_encrip
                mensaje = "Contraseña Actualizada Correctamente"
                db.session.commit()
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_info'))
            else:
                mensaje="Error , Contraseña Nueva No Coincide"
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_info'))
        else:
            mensaje="Error Verifique Contraseña Antigua"
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_info'))

@admin_bp.route('/admin_historial_atencion', methods=['GET','POST'])
def admin_historial_atencion():
    if request.method == 'GET':
        #Valida nivel de usuario
        iduservet = session['iduservet']
        datos = Uservet.query.all()
        return render_template("/app/admin_historial_atencion.html",datos=datos)   

@admin_bp.route('/admin_veterinaria', methods=['GET','POST'])
def admin_veterinaria():
    form_veterinaria = Veterinaria()
    form_foto = VeterinariaFoto()
    mensaje=''
    iduservet = session['iduservet']
    #id de vet registrada
    usuario = Uservet.query.filter_by(iduservet=iduservet).first()  
    us_vet = usuario.vet_id  
    vets = Vet.query.filter_by(idvet=us_vet).first()
    hora = datetime.datetime.now().strftime("%Y%m%d%H%M%S") 
    if vets:
        diccionario = {'logo' : vets.logo, 'imagen' : vets.imagen , 'vetid' : us_vet ,'nombre' : vets.nombre , 'telefono' : vets.telefono , 'whatsapp' : vets.whatsapp ,
        'ciudad':  vets.ciudad , 'distrito': vets.distrito , 'direccion': vets.direccion}
    else:
        diccionario = {}
    if request.method == 'GET':
        return render_template("/app/admin_veterinaria.html" , form_veterinaria=form_veterinaria , form_foto=form_foto , diccionario=diccionario)  

    if form_veterinaria.validate_on_submit():
        nombre = form_veterinaria.nombre.data
        #logo2 = request.files.get("logo",False) 
        logo = form_veterinaria.logo.data 
        telefono =form_veterinaria.telefono.data
        whatsapp = form_veterinaria.whatsapp.data 
        ciudad = form_veterinaria.ciudad.data 
        distrito = form_veterinaria.distrito.data 
        direccion = form_veterinaria.direccion.data
        imagen = None
        acceso = None 
        creado = None 

        #Si No Selecciono Archivo
        if request.files['logo'].filename == '':
            nombre_unico = None
            #Chekear en BD si ya tiene imagen asignada.
        else : 
            logo_nombre = secure_filename(logo.filename)    
            comparar=str(logo_nombre)
            #extension
            extension = os.path.splitext(comparar)

            resultado=comparar.endswith(extensiones)
            #Si el Archivo no es permitido
            if resultado == False:
                mensaje='Error Archivo debe ser extension jpg , jpeg o png'
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_veterinaria'))   
            nombre_unico = str(iduservet) + '_logo' + hora + extension[1] 
        if us_vet is None:
            nuevo_vet = Vet(nombre,nombre_unico,imagen,telefono,whatsapp,acceso,ciudad,distrito,direccion,creado)
            try:
                db.session.add(nuevo_vet)
                db.session.flush()
                id_veterinaria = nuevo_vet.idvet
                usuario.vet_id = id_veterinaria
                db.session.commit()
                mensaje='Veterinaria agregada Correctamente'
                if nombre_unico is not None:
                    logo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_unico))
                    mensaje = mensaje + ' , Se Cargo la Imagen'
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_veterinaria'))
            except exc.SQLAlchemyError as e:
                mensaje='Ocurrio Un Problema Consulte con Soporte'
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_veterinaria'))
        else:
            mivet = Vet.query.filter_by(idvet=us_vet).first() 
            #Si field esta vacio. No Actualizar ruta imagen
            #Si Field esta lleno. PRoceso de subir archivo y llenar BD.
            if request.files['logo'].filename == '':
                pass 
            else: 
                nombre_unico = str(iduservet) + '_logo' + hora + extension[1] 
                logo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_unico))
                mivet.logo = nombre_unico
            mivet.nombre = nombre 
            mivet.telefono = telefono
            mivet.whatsapp = whatsapp
            mivet.ciudad = ciudad
            mivet.distrito = distrito
            mivet.direccion = direccion
            try:
                db.session.commit()
                mensaje='Se Actualizaron los Datos de la Veterinaria'
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_veterinaria'))
            except exc.SQLAlchemyError as e:
                mensaje='Ocurrio Un Problema Reintente o Consulte con Soporte'
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_veterinaria'))
    
    if form_foto.validate_on_submit():
        foto = form_foto.foto.data 
        foto_nombre = secure_filename(foto.filename)    
        comparar=str(foto_nombre)
        #extension
        extension = os.path.splitext(comparar)
        resultado=comparar.endswith(extensiones)
        #Si el Archivo no es permitido
        if resultado == False:
            mensaje='Error Foto debe ser extension jpg , jpeg o png'
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_veterinaria'))
        nombre_unico = str(iduservet) + '_foto' + hora + extension[1]
        mivet = Vet.query.filter_by(idvet=us_vet).first()
        mivet.imagen=nombre_unico
        try:
            db.session.commit()
            foto.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_unico))
            mensaje='Foto Actualizada'
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_veterinaria'))
        except exc.SQLAlchemyError as e:
                mensaje='Ocurrio Un Problema Reintente o Consulte con Soporte'
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_veterinaria'))
        return redirect(url_for('admin_bp.admin_veterinaria'))
    else:
        mensaje='Error Debe Seleccionar una Foto'
        flash(mensaje)
        return redirect(url_for('admin_bp.admin_veterinaria'))


@admin_bp.route('/admin_cm/', methods=['GET','POST'] )
def admin_cm():
    mensaje=''
    vet =  session['iduservet'] 
    form_cliente = ClienteForm()
    form_mascota = MascotaForm()
    form_dni = BuscarCM()

    if  form_cliente.validate():
        dni = form_cliente.dni.data
        nombre = form_cliente.nombre.data 
        apellidos = form_cliente.apellidos.data 
        telefono = form_cliente.telefono.data 
        email = form_cliente.email.data 
        registradopor = vet
        existe2 = Cliente.query.filter_by(dni=dni).first()
        if existe2 is None: 
            try:
                nuevo_cliente = Cliente(nombre,apellidos,dni,email,telefono,registradopor)
                db.session.add(nuevo_cliente)
                db.session.commit()
                mensaje = "Cliente Registrado Correctamente"  
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_dni', dni=nuevo_cliente.dni))
            except exc.SQLAlchemyError as e:
                mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_cm'))      
        else: 
            existe2.nombre=form_cliente.nombre.data 
            existe2.apellido=form_cliente.apellidos.data 
            existe2.telefono=form_cliente.telefono.data
            existe2.email=form_cliente.email.data
            try:
                db.session.commit()
                mensaje='Se Actualizaron los Datos del Cliente'
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_dni',dni=existe2.dni))
            except exc.SQLAlchemyError as e:
                mensaje='Ocurrio Un Problema Reintente o Consulte con Soporte'
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_cm'))
    if form_mascota.validate_on_submit():
        id_cliente = form_mascota.dni.data
        nombre= form_mascota.nombre.data 
        raza = form_mascota.raza.data
        tipo = form_mascota.tipo.data 
        nacimiento = form_mascota.nacimiento.data
        peso = form_mascota.peso.data 
        observaciones = form_mascota.observaciones.data
        try:
            micliente = Cliente.query.filter_by(idcliente=id_cliente).first()
            print(micliente.dni)
            nueva_mas = Mascota(id_cliente,nombre,tipo,raza,nacimiento,peso,observaciones)
            db.session.add(nueva_mas)
            db.session.commit()
            mensaje = "Se Agrego a La Mascota : " + nueva_mas.nombre + " Del Cliente : " + micliente.nombre
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_dni', dni=micliente.dni))
        except exc.SQLAlchemyError as e:
            mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_cm')) 
        return redirect(url_for('admin_bp.admin_cm'))
    return render_template("/app/admin_cm.html" , form_cliente = form_cliente , form_mascota = form_mascota)   

@admin_bp.route('/admin_atencion', methods=['GET','POST'])
def admin_atencion():
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    form_dni = AtencionDNI()
    form_atencion = AtencionForm()
    estado_atencion="abierto"
    if request.method == "POST":
        token = form_atencion.csrf_token.data
        id_cliente = form_atencion.id_cliente.data 
        mascota = form_atencion.mascota.data 
        sintomas = form_atencion.sintomas.data 
        informe = form_atencion.informe.data 
        receta = form_atencion.receta.data 
        observaciones = form_atencion.observaciones.data
        fecha_atencion = None 
        total = 0
        atendido_por = form_atencion.atendido_por.data
        usuario = Uservet.query.filter_by(iduservet=iduservet).first()
        creado_por = usuario.nombre
        estado_atencion = "abierto"
        try:
            nueva_atencion = Atencion(fecha_atencion,receta,sintomas,informe,observaciones,mascota,total,id_cliente,usuario.vet_id,atendido_por,creado_por,estado_atencion)
            db.session.add(nueva_atencion)
            db.session.commit()
            mensaje = "Atencion Creada !"
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_atencion'))
        except exc.SQLAlchemyError as e:
            mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_atencion'))
    atenciones = Atencion.query.with_entities(Atencion.idatencion,Atencion.fecha_atencion,Atencion.total,Atencion.nombremascota,Atencion.creado_por,Atencion.estado_atencion).filter_by(idvet=idvet).filter_by(estado_atencion=estado_atencion).join(Cliente, Atencion.idcliente==Cliente.idcliente).add_columns(Cliente.nombre , Cliente.apellidos).order_by(Atencion.fecha_atencion.desc()).limit(5).all()
    return render_template("/app/admin_atencion.html",form_dni=form_dni,form_atencion=form_atencion,atenciones=atenciones)


@admin_bp.route('/admin_dni_atencion', methods=['GET','POST'])
def admin_dni_atencion(result=None):
    idvet = session['vet_id']
    mensaje=''
    estado_atencion="abierto"
    form_atencion = AtencionForm()
    if request.args.get('dni',None):
        result = request.args.get('dni')
        existe = Cliente.query.filter_by(dni=result).first()
        if existe is None:
           mensaje='El Cliente No Existe Porfavor Registre el DNI : ' + result
           flash(mensaje)
           return redirect(url_for('admin_bp.admin_cm'))
        else:
            mascotas = Mascota.query.filter_by(idcliente=existe.idcliente).all()
            if not mascotas:
                mensaje=' Porfavor Registre Al menos una Mascota del Cliente ' + str(existe.dni) + '  ' + str(existe.nombre)
                flash(mensaje)
                return redirect(url_for('admin_bp.admin_cm')) 
            form_atencion.buscar_mascota(existe.idcliente)
            form_atencion.buscar_empleado(idvet)
            diccionario = {'dni' : existe.dni, 'nombre' : existe.nombre , 'apellidos' : existe.apellidos, 'id_cliente' : existe.idcliente }
            mensaje='Cliente encontrado'
            flash(mensaje)
            return render_template("/app/admin_atencion.html",diccionario=diccionario,form_atencion=form_atencion)
    atenciones = Atencion.query.with_entities(Atencion.idatencion,Atencion.fecha_atencion,Atencion.total,Atencion.nombremascota,Atencion.creado_por,Atencion.estado_atencion).filter_by(idvet=idvet).filter_by(estado_atencion=estado_atencion).join(Cliente, Atencion.idcliente==Cliente.idcliente).add_columns(Cliente.nombre , Cliente.apellidos).order_by(Atencion.fecha_atencion.desc()).limit(5).all()
    return render_template("app/admin_atencion.html",atenciones=atenciones,form_atencion=form_atencion)

@admin_bp.route('/admin_dni', methods=['GET','POST'])
def admin_dni(result=None):
    form_cliente = ClienteForm()
    form_mascota = MascotaForm()
    if request.args.get('dni',None):
        result=request.args.get('dni')
        existe = Cliente.query.filter_by(dni=result).first()  
        if existe is None:
            mensaje='El Cliente No Existe Porfavor Registre el DNI : ' + result
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_cm'))
        else:
            mascotas = Mascota.query.filter_by(idcliente=existe.idcliente).all()
            diccionario = {'dni' : existe.dni, 'nombre' : existe.nombre , 'apellidos' : existe.apellidos ,'telefono' : existe.telefono , 'email' : existe.email , 'id' : existe.idcliente }
            return render_template("/app/admin_cm.html",diccionario=diccionario,form_cliente=form_cliente,form_mascota=form_mascota,mascotas=mascotas)
    return redirect(url_for('admin_bp.admin_cm'))

@admin_bp.route('/eliminar_mascota/<id>', methods=['GET','POST'])
def eliminar_mascota(id):
    idmascota = id
    try:
        datos =  Mascota.query.filter_by(idmascota=idmascota).first()
        dueno = Cliente.query.filter_by(idcliente=datos.idcliente).first()
        Mascota.query.filter_by(idmascota=idmascota).delete()
        db.session.commit()
        mensaje = "Mascota eliminada"
        flash(mensaje)
        return redirect(url_for('admin_bp.admin_dni', dni=dueno.dni))
    except exc.SQLAlchemyError as e:
        mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
        flash(mensaje)
        return redirect(url_for('admin_bp.admin_cm')) 

@admin_bp.route('/editar_mascota/', methods=['GET','POST'] , defaults={'id':None})
@admin_bp.route('/editar_mascota/<int:id>', methods=['GET','POST'])
def editar_mascota(id):
    id_mascota = id 
    form_mascota = MascotaFormUpd()
    if request.method == "GET":  
        datos = Mascota.query.filter_by(idmascota=id_mascota).first()
        return render_template("app/admin_updmascota.html" , form_mascota= form_mascota , datos=datos)
    if form_mascota.validate_on_submit() and id is None:
        idmascota = form_mascota.id_mascota.data
        nombre = form_mascota.nombre.data 
        raza = form_mascota.raza.data 
        tipo = form_mascota.tipo.data 
        nacimiento = form_mascota.nacimiento.data 
        peso = form_mascota.peso.data 
        observaciones = form_mascota.observaciones.data 
        #Obtener DNI a partir de IDMASCOTA.
        data = Cliente.query.with_entities(Cliente.dni).join(Mascota, Cliente.idcliente == Mascota.idcliente).filter_by(idmascota=idmascota).one()
        try : 
            mimascota = Mascota.query.filter_by(idmascota=idmascota).first()
            mimascota.nombre = nombre 
            mimascota.raza = raza 
            mimascota.tipo = tipo 
            mimascota.nacimiento = nacimiento 
            mimascota.peso = peso 
            mimascota.observaciones = observaciones 
            db.session.commit()
            mensaje = "Datos Actualizados"
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_dni', dni=data.dni, form_mascota=form_mascota))
        except exc.SQLAlchemyError as e:
            mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
            flash(mensaje)
            return redirect(url_for('admin_bp.admin_cm')) 
        return redirect(url_for('admin_bp.admin_dni', dni=data.dni, form_mascota=form_mascota))
    return "Porfavor Reinicie la aplicacion"
        

@admin_bp.route('/editar_atencion/', methods=['GET','POST'] , defaults={'id':None})
@admin_bp.route('/editar_atencion/<int:id>', methods=['GET','POST'])
def editar_atencion(id):
    id_atencion = id 
    if request.method == "GET":  
        datos = AtencionDetalle.query.filter_by(idatencion=id_atencion).all()
        #datos_atencion = Atencion.query.filter_by(idatencion=id_atencion).first()
        print(datos)
        return render_template("app/admin_editar_atencion.html" , datos=datos)
    return "test"

@admin_bp.route('/terminar_atencion/<int:id>', methods=['GET','POST'])
def terminar_atencion(id):
    id_atencion = id 
    print(id_atencion)
    return "test"

    