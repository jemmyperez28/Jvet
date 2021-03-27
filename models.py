from sqlalchemy import Column, Integer, DateTime , func , MetaData , Float
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
    servicio = db.Column(db.String(100))
    otro = db.Column(db.String(250))
    costo = db.Column(db.Float)
    idatencion = db.Column(db.Integer,db.ForeignKey('atencion.idatencion'))
    def __init__(self,servicio,otro,costo,idatencion):
        self.servicio = servicio 
        self.otro = otro
        self.costo = costo
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
    relacionatenciondetalle = db.relationship('AtencionDetalle',backref='atencion',lazy=True)
    def __init__(self,fecha_atencion,receta,sintomas,informe,observaciones,nombremascota,total,idcliente,idvet):
        self.fecha_atencion = fecha_atencion 
        self.receta = receta
        self.sintomas = sintomas
        self.informe = informe
        self.observaciones = observaciones
        self.nombremascota=nombremascota
        self.total = total
        self.idcliente = idcliente
        self.idvet = idvet














    





  


    










       