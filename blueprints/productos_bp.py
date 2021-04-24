from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from forms import NuevoProducto
from models import Productos, Kardex
from sqlalchemy import exc , desc , func
productos_bp = Blueprint('productos_bp',__name__)

@productos_bp.route('/admin_productos', methods=['GET','POST'])
def admin_productos():
    mensaje=''
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    if request.method == 'GET':
        datos = Productos.query.filter_by(idvet=idvet).all()
        return render_template("/app/mis_productos.html",datos=datos)

@productos_bp.route('/admin_nuevo_producto', methods=['GET','POST'])
def admin_nuevo_producto():
    mensaje=''
    iduservet =  session['iduservet'] 
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    form_producto2 = NuevoProducto()
    if request.method == 'GET':
        return render_template("/app/nuevo_producto.html", form_producto2=form_producto2)
    if form_producto2.validate_on_submit():
        nombre = form_producto2.nombre_producto.data 
        descripcion = form_producto2.descripcion_producto.data 
        precio = form_producto2.precio_producto.data 
        stock = form_producto2.stock_producto.data 
        try:
            #Agregar a tabla producto.
            nuevo_producto = Productos(nombre,descripcion,precio,stock,idvet)
            db.session.add(nuevo_producto)
            db.session.flush()
            #Ingresar Registro en Kardex
            nuevo_kardex = Kardex(None,'Nuevo',nombre_usuario,nuevo_producto.nombre,nuevo_producto.stock,0,idvet,None,None)
            db.session.add(nuevo_kardex)
            db.session.commit()
            mensaje = "Nuevo Producto Añadido , Codigo del Producto : " + str(nuevo_producto.idProducto)
            flash(mensaje)
            return redirect(url_for('productos_bp.admin_nuevo_producto'))
        except exc.SQLAlchemyError as e:
            mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
            flash(mensaje)
            return redirect(url_for('productos_bp.admin_nuevo_producto'))
    return "Reinicie app 39productosbp"