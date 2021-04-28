from sqlalchemy import Column, Integer, DateTime , func , MetaData , Float , UniqueConstraint , Date
from datetime import datetime
from config.db import db

class Vet(db.Model):
    idvet = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    logo = db.Column(db.String(200))
    imagen = db.Column(db.String(200))
    telefono = db.Column(db.String(100))
    whatsapp = db.Column(db.String(100))
    acceso = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    distrito = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    creado = db.Column(db.DateTime,default=datetime.utcnow)
    uservets = db.relationship('Uservet',backref='vet',lazy=True)
    relacionservicios = db.relationship('Servicios',backref='vet',lazy=True)
    relacionatencion = db.relationship('Atencion',backref='vet',lazy=True)
    relacionempleado = db.relationship('Empleado',backref='vet',lazy=True)
    relacionproductos = db.relationship('Productos',backref='vet',lazy=True)
    relacionkardex = db.relationship('Kardex',backref='vet',lazy=True)
    relacionreservacion = db.relationship('Reservacion',backref='vet',lazy=True)

    def __init__(self,nombre,logo,imagen,telefono,whatsapp,acceso,ciudad,distrito,direccion,creado):
        self.nombre = nombre
        self.logo = logo
        self.imagen = imagen
        self.telefono = telefono
        self.whatsapp = whatsapp
        self.acceso = acceso
        self.ciudad = ciudad
        self.distrito = distrito
        self.direccion = direccion    
        self.creado = creado 

class Uservet(db.Model):
    iduservet = db.Column(db.Integer, primary_key = True)
    dni = db.Column(db.Integer , nullable = False , unique=True)
    email = db.Column(db.String(200), nullable = True , unique=True)
    password = db.Column(db.String(250), nullable = False)
    nombre = db.Column(db.String(250))
    apellidos = db.Column(db.String(250))
    telefono = db.Column(db.String(250))
    tipo_uservet = db.Column(db.String(250))
    estado_uservet = db.Column(db.String(250))
    validado = db.Column(db.String(250))
    creado = db.Column(db.DateTime,default=datetime.utcnow)
    vet_id = db.Column(db.Integer,db.ForeignKey('vet.idvet'))
    idsuscripcion = db.Column(db.Integer,db.ForeignKey('suscripcion.idsuscripcion'))
    idvendedor = db.Column(db.Integer,db.ForeignKey('vendedor.idvendedor'))

    def __init__(self,dni,email,password,nombre,apellidos,telefono,tipo_uservet,estado_uservet,validado,creado,vet_id):
        self.dni = dni 
        self.email = email
        self.password = password
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = telefono
        self.tipo_uservet = tipo_uservet
        self.estado_uservet = estado_uservet
        self.validado = validado
        self.creado = creado
        self.vet_id = vet_id

class Suscripcion(db.Model):
    idsuscripcion = db.Column(db.Integer, primary_key = True)
    tipo = db.Column(db.String(250))
    fecha_renovacion = db.Column(db.DateTime)
    fecha_vencimiento = db.Column(db.DateTime)
    relacionuservet = db.relationship('Uservet',backref='suscripcion',lazy=True)
    def __init__(self,tipo,fecha_renovacion,fecha_vencimiento):
        self.tipo = tipo 
        self.fecha_renovacion = fecha_renovacion
        self.fecha_vencimiento = fecha_vencimiento

class Vendedor(db.Model):
    idvendedor = db.Column(db.Integer, primary_key = True)
    dni = db.Column(db.Integer , nullable = False , unique=True)
    email = db.Column(db.String(200), nullable = True , unique=True)
    password = db.Column(db.String(250), nullable = False)
    nombre = db.Column(db.String(250))
    apellidos = db.Column(db.String(250))
    telefono = db.Column(db.String(250))
    banco = db.Column(db.String(250))
    nro_cuenta = db.Column(db.String(250))
    relacionuservet = db.relationship('Uservet',backref='vendedor',lazy=True)
    def __init__(self,dni,email,password,nombre,apellidos,telefono,banco,nro_cuenta):
        self.dni = dni 
        self.email = email
        self.password = password
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = telefono
        self.banco = banco
        self.nro_cuenta = nro_cuenta

class Servicios(db.Model):
    idServicio = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(250))
    tipo = db.Column(db.String(250))
    precio = db.Column(db.Float)
    detalles = db.Column(db.String(250))
    idvet = db.Column(db.Integer,db.ForeignKey('vet.idvet'))
    def __init__(self,nombre,tipo,precio,detalles,idvet):
        self.nombre = nombre 
        self.tipo = tipo
        self.precio = precio
        self.detalles = detalles
        self.idvet = idvet

class Productos(db.Model):
    idProducto = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(250))
    descripcion = db.Column(db.String(250))
    precio = db.Column(db.Float)
    stock = db.Column(db.Integer)
    idvet = db.Column(db.Integer,db.ForeignKey('vet.idvet'))
    __table_args__ = (db.UniqueConstraint('nombre','idvet'),)

    def __init__(self,nombre,descripcion,precio,stock,idvet):
        self.nombre = nombre 
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.idvet = idvet


class Cliente(db.Model):
    idcliente = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(250))
    apellidos = db.Column(db.String(250))
    dni = db.Column(db.Integer, unique=True )
    email = db.Column(db.String(250))
    telefono = db.Column(db.String(250))
    registradopor = db.Column(db.String(250))
    relacionmascota = db.relationship('Mascota',backref='cliente',lazy=True)
    relacionatencion = db.relationship('Atencion',backref='cliente',lazy=True)
    def __init__(self,nombre,apellidos,dni,email,telefono,registradopor):
        self.nombre = nombre 
        self.apellidos = apellidos
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.registradopor = registradopor

class Mascota(db.Model):
    idmascota =  db.Column(db.Integer, primary_key = True)
    idcliente = db.Column(db.Integer,db.ForeignKey('cliente.idcliente'))
    nombre = db.Column(db.String(250))
    tipo = db.Column(db.String(250))
    raza = db.Column(db.String(250))
    nacimiento = db.Column(db.Date)
    peso = db.Column(db.String(250))
    observaciones = db.Column(db.String(1000))
    def __init__(self,idcliente,nombre,tipo,raza,nacimiento,peso,observaciones):
        self.idcliente = idcliente
        self.nombre = nombre 
        self.tipo = tipo
        self.raza = raza
        self.nacimiento = nacimiento
        self.peso = peso
        self.observaciones = observaciones

class AtencionDetalle(db.Model):
    idatenciondetalle = db.Column(db.Integer, primary_key = True)
    tipo = db.Column(db.String(100))
    nombre = db.Column(db.String(250))
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    idatencion = db.Column(db.Integer,db.ForeignKey('atencion.idatencion'))
    def __init__(self,tipo,nombre,cantidad,precio_unitario,subtotal,idatencion):
        self.tipo = tipo 
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
        self.idatencion = idatencion

class Atencion(db.Model):
    idatencion = db.Column(db.Integer, primary_key = True)
    fecha_atencion = db.Column(db.DateTime,default=datetime.utcnow)
    receta = db.Column(db.String(300))
    sintomas = db.Column(db.String(300))
    informe = db.Column(db.String(300))
    observaciones = db.Column(db.String(300))
    nombremascota = db.Column(db.String(100))
    total = db.Column(db.Float)
    idcliente = db.Column(db.Integer,db.ForeignKey('cliente.idcliente'))
    idvet = db.Column(db.Integer,db.ForeignKey('vet.idvet'))
    atendido_por = db.Column(db.String(100))
    creado_por = db.Column(db.String(100))
    estado_atencion = db.Column(db.String(100))
    nombre_apellido = db.Column(db.String(100))
    dni = db.Column(db.String(20))
    email = db.Column(db.String(100))
    idreservacion = db.Column(db.Integer)
    relacionatenciondetalle = db.relationship('AtencionDetalle',backref='atencion',lazy=True)
    def __init__(self,fecha_atencion,receta,sintomas,informe,observaciones,nombremascota,total,idcliente,idvet,atendido_por,creado_por,estado_atencion,nombre_apellido,dni,email):
        self.fecha_atencion = fecha_atencion 
        self.receta = receta
        self.sintomas = sintomas
        self.informe = informe
        self.observaciones = observaciones
        self.nombremascota=nombremascota
        self.total = total
        self.idcliente = idcliente
        self.idvet = idvet
        self.atendido_por = atendido_por
        self.creado_por = creado_por
        self.estado_atencion = estado_atencion
        self.nombre_apellido = nombre_apellido
        self.dni = dni 
        self.email = email

class Empleado(db.Model):
    idempleado = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(300))
    dni = db.Column(db.String(100))
    password = db.Column(db.String(100))
    atencion = db.Column(db.String(1))
    petshop = db.Column(db.String(1))
    reservaciones = db.Column(db.String(1))
    servicios = db.Column(db.String(1))
    productos = db.Column(db.String(1))
    activo = db.Column(db.String(2))
    idvet = db.Column(db.Integer,db.ForeignKey('vet.idvet'))
    def __init__(self,nombre,dni,password,atencion,petshop,reservaciones,servicios,productos,activo,idvet):
        self.nombre = nombre 
        self.dni = dni
        self.password = password
        self.atencion = atencion
        self.petshop = petshop
        self.reservaciones=reservaciones
        self.servicios = servicios
        self.productos = productos
        self.activo = activo
        self.idvet = idvet

class Kardex(db.Model):
    idkardex = db.Column(db.Integer,primary_key=True)
    fecha_kardex = db.Column(db.DateTime,default=datetime.utcnow)
    tipo = db.Column(db.String(30))
    usuario = db.Column(db.String(50))
    producto = db.Column(db.String(50))
    cantidad_ingreso = db.Column(db.Integer)
    cantidad_salida = db.Column(db.Integer)
    idvet = db.Column(db.Integer,db.ForeignKey('vet.idvet'))
    idatedet = db.Column(db.Integer , unique=True)
    idordendet = db.Column(db.Integer , unique = True)
    def __init__(self,fecha_kardex,tipo,usuario,producto,cantidad_ingreso,cantidad_salida,idvet,idatedet,idordendet):
        self.fecha_kardex=fecha_kardex
        self.tipo=tipo
        self.usuario=usuario
        self.producto=producto
        self.cantidad_ingreso=cantidad_ingreso
        self.cantidad_salida=cantidad_salida
        self.idvet=idvet 
        self.idatedet=idatedet
        self.idordendet=idordendet

class Reservacion(db.Model):
    idreservacion = db.Column(db.Integer,primary_key=True)
    idvet = db.Column(db.Integer,db.ForeignKey('vet.idvet'))
    dni = db.Column(db.String(20))
    nombre_apellido = db.Column(db.String(100))
    telefono = db.Column(db.String(100))
    email = db.Column(db.String(100))
    fecha = db.Column(db.Date)
    hora_inicio = db.Column(db.String(20))
    hora_final = db.Column(db.String(20))
    observacion = db.Column(db.String(100))
    encargado = db.Column(db.String(100))
    estado_reservacion = db.Column(db.String(100)) 
    def __init__(self,idvet,dni,nombre_apellido,telefono,email,fecha,hora_inicio,hora_final,observacion,encargado,estado_reservacion):
        self.idvet=idvet
        self.dni=dni
        self.nombre_apellido=nombre_apellido
        self.telefono=telefono
        self.email=email 
        self.fecha=fecha
        self.hora_inicio = hora_inicio 
        self.hora_final = hora_final 
        self.observacion = observacion
        self.encargado = encargado
        self.estado_reservacion = estado_reservacion

class Hora(db.Model):
    idhora = db.Column(db.Integer,primary_key=True)
    hora = db.Column(db.String(100))
    def __init__(self,hora):
        self.hora=hora















    





  


    










       