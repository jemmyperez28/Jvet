from flask import Blueprint , render_template , request , flash ,redirect , url_for , session
from forms import RegistroUsuario , LoginUsuario
from schemas import UserVetSchema
from config.db import db
from models import Uservet
from sqlalchemy import exc
from funciones import encriptar

UserVet_Schema = UserVetSchema()
UserVets_Schema = UserVetSchema(many=True)

login = Blueprint('login',__name__)

@login.route('/registro_usuario', methods=['GET','POST'])
def registro_usuario():
    mensaje = ''
    registro_usuario = RegistroUsuario()
    if registro_usuario.validate_on_submit():
        dni = registro_usuario.dni.data
        nombre = registro_usuario.nombre.data
        email = registro_usuario.email.data
        password1 = registro_usuario.password1.data
        password2 = registro_usuario.password2.data
        apellidos = registro_usuario.apellidos.data
        telefono = registro_usuario.telefono.data
        tipo_uservet = "admin"
        estado_uservet = "creado"
        validado = "Falso"
        idvet = None
        creado = None 
        
        if password1==password2:
            password=encriptar(password1)
            nuevo_uservet = Uservet(dni,email,password,nombre,apellidos,telefono,tipo_uservet,estado_uservet,validado,creado,idvet)
            try:
                db.session.add(nuevo_uservet)
                db.session.commit()
                mensaje = "Registro Exitoso"
                flash(mensaje)
                return redirect(url_for('login.login_usuario'))
            except exc.SQLAlchemyError as e:
                mensaje = "Error : " + str(e._sql_message) + "Consulte con Soporte " 
                flash(mensaje)
                return redirect(url_for('login.registro_usuario'))
        else : 
            mensaje = "Error , Contraseñas no son Iguales"
            flash(mensaje)
            return redirect(url_for('login.registro_usuario'))
    return render_template("/login/registro_usuario.html" , registro_usuario=registro_usuario)


@login.route('/login_usuario', methods=['GET','POST'])
def login_usuario():
    mensaje =''
    login_usuario=LoginUsuario(request.form)
    #if login_usuario.validate_on_submit():
    if request.method == 'POST' and login_usuario.validate():
        email = login_usuario.email.data 
        password_data = login_usuario.password.data
        password=encriptar(password_data)
        #Comprobacion 
        usuario = Uservet.query.filter_by(email=email).first()
        if not usuario : 
            mensaje  ="Error , El Correo Ingresado no Existe"
            flash(mensaje)
            return redirect(url_for('login.login_usuario'))
        else : 
            if password == usuario.password:
                session['loggedin'] = True 
                session['iduservet'] = usuario.iduservet
                session['dni'] = usuario.dni
                session['nombre'] = usuario.nombre
                session['tipo_uservet'] = usuario.tipo_uservet
                if usuario.tipo_uservet == "admin":
                    return redirect(url_for('admin_bp.index_admin'))
            else:
                mensaje  = "Error , Contraseña Incorrecta"
                flash(mensaje)
                return redirect(url_for('login.login_usuario'))

    return render_template("/login/login_usuario.html", login_usuario=login_usuario) 

@login.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('login.login_usuario'))


    

    