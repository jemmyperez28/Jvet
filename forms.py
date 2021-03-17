from flask_wtf import FlaskForm 
from wtforms import StringField , PasswordField , IntegerField , SubmitField , FileField , SelectField
from wtforms.validators import InputRequired

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
    



   



