from flask_wtf import FlaskForm 
from wtforms.fields.html5 import DateField
from wtforms import StringField , PasswordField , IntegerField , SubmitField , FileField , SelectField  , TextAreaField , HiddenField , FloatField
from wtforms.validators import InputRequired
from models import Mascota , Empleado , Uservet , Servicios , Productos , Hora


class ModificarVet(FlaskForm):
    id = HiddenField('id')
    mensaje = StringField('mensaje')
    vision = StringField('vision')
    mision = StringField('mision')
    nombre_unico = StringField('nombre_unico')
    clave_reporte = StringField('clave_reporte')

class ModificarUsuario(FlaskForm):
    id = HiddenField('id')
    clave = StringField('clave')
    validado = StringField('validado')


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

class LoginSuper(FlaskForm):
    user = StringField('user',validators=[InputRequired()])
    pass1 = PasswordField('pass1',validators=[InputRequired()])
    pass2 = PasswordField('pass2',validators=[InputRequired()])

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

class ForgotPassword2(FlaskForm):
    password_old = StringField('password_old',validators=[InputRequired()])
    password1 = PasswordField('password1',validators=[InputRequired()])
    password2 = PasswordField('password2',validators=[InputRequired()])


class Veterinaria(FlaskForm):
    nombre = StringField('nombre',validators=[InputRequired()])
    logo = FileField('logo')
    telefono = StringField('nombre',validators=[InputRequired()])
    whatsapp = StringField('nombre',validators=[InputRequired()])
    ciudad = SelectField("ciudad" , choices=[("Lima","Callao")])
    distrito = SelectField("distrito" , choices=[("San Juan de Lurigancho","Lurigancho")])
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

class AtencionForm2(FlaskForm):
    #id_cliente = HiddenField('id_cliente',validators=[InputRequired()])
    #mascota = SelectField(coerce=str)
    #mascota = SelectField('mascota',coerce=int)
    dni = StringField('dni')
    nombre_apellidos = StringField('nombre_apellidos')
    mascota = StringField('mascota')
    email = StringField('email')
    atendido_por = SelectField('atendido_por',coerce=str)
    sintomas = TextAreaField('sintomas')
    informe = TextAreaField('informe')
    receta = TextAreaField('receta')
    observaciones = TextAreaField('observaciones')
    def buscar_empleado(self,idvet):
        self.atendido_por.choices = [(empleado.nombre, empleado.nombre) for empleado in Empleado.query.filter_by(idvet=idvet).all()]


class AtencionServicioForm(FlaskForm):
    precio = SelectField('precio',coerce=float)
    idatencion = HiddenField('idatencion')
    nombre = StringField('nombre')
    nombre2 = HiddenField('nombre2') 
    cantidad = IntegerField('cantidad')

    def buscar_servicios(self,idvet):
        self.precio.choices = [(servicio.precio,servicio.nombre) for servicio in Servicios.query.filter_by(idvet=idvet).all()]  

class AtencionProductoForm(FlaskForm):
    precio_producto = SelectField('precio_producto',coerce=float)
    idatencion_producto = HiddenField('idatencion')
    nombre_producto = StringField('nombre_producto')
    nombre2_producto = HiddenField('nombre2_producto') 
    cantidad_producto = IntegerField('cantidad_producto')

    def buscar_productos(self,idvet):
        self.precio_producto.choices = [(producto.precio,producto.nombre) for producto in Productos.query.filter_by(idvet=idvet).all()]   

class AtencionOtroForm(FlaskForm):
    idatencion_otro = HiddenField('idatencion')
    otro = StringField('otro')     
    precio = FloatField('precio')
    cantidad = IntegerField('cantidad')

class AtencionPadre(FlaskForm):
    idatencion = HiddenField('idatencion')
    sintomas = TextAreaField('sintomas')
    informe = TextAreaField('informe')
    receta =  TextAreaField('receta')
    observaciones = TextAreaField('observaciones')
class BuscarAtencion(FlaskForm):
    dni = IntegerField('dni')
    fecha = DateField('fecha')

class BuscarReservacion(FlaskForm):
    fecha = DateField('fecha')

class NuevoProducto(FlaskForm):
    nombre_producto = StringField('nombre_producto',validators=[InputRequired()])
    descripcion_producto = StringField('descripcion_producto',validators=[InputRequired()])
    precio_producto = FloatField('precio_producto',validators=[InputRequired()])
    stock_producto = IntegerField('stock_producto',validators=[InputRequired()])

class StockForm(FlaskForm):
    idproducto = HiddenField('idproducto',validators=[InputRequired()])
    aumento = IntegerField('aumento',validators=[InputRequired()])

class ModificarProducto(FlaskForm):
    idproducto = HiddenField('idproducto',validators=[InputRequired()])
    nombre_producto = StringField('nombre_producto')
    descripcion_producto = StringField('descripcion_producto')
    precio_producto = FloatField('precio_producto')
class NuevoServicio(FlaskForm):
    nombre_servicio = StringField('nombre_servicio',validators=[InputRequired()])
    tipo_servicio = StringField('tipo_servicio',validators=[InputRequired()])
    precio_servicio = StringField('precio_servicio',validators=[InputRequired()])
    detalles_servicio = StringField('detalles_servicio',validators=[InputRequired()])
class ModificarServicio(FlaskForm):
    idservicio = HiddenField('idservicio',validators=[InputRequired()])
    nombre_servicio = StringField('nombre_servicio')
    tipo_servicio = StringField('tipo_servicio')
    precio_servicio = StringField('precio_servicio')
    detalles_servicio = StringField('detalles_servicio')

class NuevaReserva(FlaskForm):
    dni = StringField('dni',validators=[InputRequired()])
    asunto = StringField('asunto',validators=[InputRequired()])
    encargado = SelectField('encargado',coerce=str,validators=[InputRequired()])
    fecha = DateField('fecha',validators=[InputRequired()])
    hora_inicio = SelectField('hora_inicio' , coerce=str,validators=[InputRequired()])
    def buscar_empleado(self,idvet):
        self.encargado.choices = [(empleado.nombre, empleado.nombre) for empleado in Empleado.query.filter_by(idvet=idvet).all()]
    def cargar_horas(self,idvet):
        self.hora_inicio.choices = [(hora.hora, hora.hora) for hora in Hora.query.all()]
class AtenderReservacion(FlaskForm):
    idreservacion =  HiddenField('idreservacion',validators=[InputRequired()])
    dni = StringField('dni',validators=[InputRequired()])
    nombre_apellido = StringField('nombre_apellido')
    email = StringField('email')
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

class EmpleadosForm(FlaskForm):
    nombre = StringField('nombre',validators=[InputRequired()])

class ReporteIngresos(FlaskForm):
    fecha_ini = DateField('fecha_ini',validators=[InputRequired()])
    fecha_fin = DateField('fecha_fin',validators=[InputRequired()])
    clave_reporte = PasswordField('clave_reporte',validators=[InputRequired()])

class PagoForm(FlaskForm):
    foto = FileField('foto',validators=[InputRequired()])
    mes = SelectField("Mes" , choices=[("Enero","Enero"),("Febrero","Febrero"),("Marzo","Marzo"),("Abril","Abril"),("Mayo","Mayo"),("Junio","Junio"),("Julio","Julio"),("Agosto","Agosto"),("Septiembre","Septiembre"),("Octubre","Octubre"),("Noviembre","Noviembre"),("Diciembre","Diciembre")] , validators=[InputRequired()]) 
    anio = StringField("anio",validators=[InputRequired()])
    monto = StringField("monto",validators=[InputRequired()])

class VendedorForm(FlaskForm):
    dni = StringField('dni')
    correo = StringField('correo')
    nombre = StringField('nombre')
    apellidos = StringField('apellidos')
    telefono = StringField('telefono')
    banco = StringField('banco')
    nro_cuenta = StringField('nro_cuenta')
    nro_cuenta_int = StringField('nro_cuenta_int')

class NuevoVendedorForm(FlaskForm):
    dni = StringField('dni')
    correo = StringField('correo')
    password = StringField('password')
    nombre = StringField('nombre')
    apellidos = StringField('apellidos')
    telefono = StringField('telefono')








        




    


   






   



