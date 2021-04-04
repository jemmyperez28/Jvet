from flask_wtf import FlaskForm 
from wtforms.fields.html5 import DateField
from wtforms import StringField , PasswordField , IntegerField , SubmitField , FileField , SelectField  , TextAreaField , HiddenField
from wtforms.validators import InputRequired
from models import Mascota , Empleado

class RegistroUsuario(FlaskForm):
    dni = IntegerField('dni')
    nombre = StringField('nombre',validators=[InputRequired()])
    apellidos = StringField('apellidos',validators=[InputRequired()])
    telefono = StringField('telefono',validators=[InputRequired()])
    idvendedor = IntegerField('idvendedor')
    email = StringField('email',validators=[InputRequired()])
    password1 = PasswordField('password1',validators=[InputRequired()])
    password2 = PasswordField('password2',validators=[InputRequired()])

class LoginUsuario(FlaskForm):
    email = StringField('email',validators=[InputRequired()])
    password = PasswordField('password',validators=[InputRequired()])

class AdminInfo(FlaskForm):
    dni = IntegerField('dni',validators=[InputRequired()])
    email = StringField('email',validators=[InputRequired()])
    nombre = StringField('nombre',validators=[InputRequired()])
    apellidos = StringField('apellidos',validators=[InputRequired()])
    telefono = StringField('telefono',validators=[InputRequired()])
    tipo_uservet = StringField('tipo_uservet',validators=[InputRequired()])

class ForgotPassword(FlaskForm):
    password_old = StringField('password_old',validators=[InputRequired()])
    password1 = PasswordField('password1',validators=[InputRequired()])
    password2 = PasswordField('password2',validators=[InputRequired()])

class Veterinaria(FlaskForm):
    nombre = StringField('nombre',validators=[InputRequired()])
    logo = FileField('logo')
    telefono = StringField('nombre',validators=[InputRequired()])
    whatsapp = StringField('nombre',validators=[InputRequired()])
    ciudad = SelectField("ciudad" , choices=[("Lima","Lima"),("Huacho","Huacho")])
    distrito = SelectField("distrito" , choices=[("San Juan de Lurigancho","San Juan de Lurigancho"),("Barrios Altos","Barrios Altos")])
    direccion = StringField('nombre',validators=[InputRequired()])

class VeterinariaFoto(FlaskForm):
    foto = FileField('foto',validators=[InputRequired()])

class ClienteForm(FlaskForm):
    dni = IntegerField('dni',validators=[InputRequired()])
    email = StringField('email')
    nombre = StringField('nombre',validators=[InputRequired()])
    apellidos = StringField('apellidos',validators=[InputRequired()])
    telefono = StringField('telefono',validators=[InputRequired()])

class MascotaForm(FlaskForm):
    dni = HiddenField('dni',validators=[InputRequired()])
    nombre = StringField('nombre',validators=[InputRequired()])
    tipo = StringField('tipo')
    raza = StringField('raza')
    nacimiento = DateField('nacimiento',validators=[InputRequired()])
    peso = StringField('peso')
    observaciones = TextAreaField('observaciones')
class MascotaFormUpd(FlaskForm):
    id_mascota = HiddenField('id_mascota',validators=[InputRequired()])
    nombre = StringField('nombre')
    tipo = StringField('tipo')
    raza = StringField('raza')
    nacimiento = DateField('nacimiento')
    peso = StringField('peso')
    observaciones = TextAreaField('observaciones')

class BuscarCM(FlaskForm):
    dni = IntegerField('dni',validators=[InputRequired()])
    submit = SubmitField('Comprobar DNI')

class AtencionDNI(FlaskForm):
    dni = IntegerField('dni',validators=[InputRequired()])

class AtencionForm(FlaskForm):
    id_cliente = HiddenField('id_cliente',validators=[InputRequired()])
    #mascota = SelectField(coerce=str)
    #mascota = SelectField('mascota',coerce=int)
    mascota = SelectField('mascota',coerce=str)
    atendido_por = SelectField('atendido_por',coerce=str)
    sintomas = TextAreaField('sintomas')
    informe = TextAreaField('informe')
    receta = TextAreaField('receta')
    observaciones = TextAreaField('observaciones')

    def buscar_mascota(self,idcliente):
        self.mascota.choices = [(mascota.nombre, mascota.nombre) for mascota in Mascota.query.filter_by(idcliente=idcliente).all()]
    
    def buscar_empleado(self,idvet):
        self.atendido_por.choices = [(empleado.nombre, empleado.nombre) for empleado in Empleado.query.filter_by(idvet=idvet).all()]




    


   






   



