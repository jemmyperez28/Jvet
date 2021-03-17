from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app
from forms import AdminInfo , ForgotPassword , Veterinaria , VeterinariaFoto
from models import Uservet , Vet
from funciones import encriptar
from config.db import db 
import os
from werkzeug.utils import secure_filename
#from config.settings import UPLOAD_FOLDER
#from config.keys import UPLOAD_FOLDER
import imghdr
from config.keys import extensiones
from sqlalchemy import exc
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
        print(datos)
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
