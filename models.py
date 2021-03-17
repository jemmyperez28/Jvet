from sqlalchemy import Column, Integer, DateTime , func , MetaData
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







       