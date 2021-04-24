from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from forms import NuevoProducto , StockForm , ModificarProducto
from models import Productos, Kardex
from sqlalchemy import exc , desc , func
productos_bp = Blueprint('productos_bp',__name__)

@productos_bp.route('/admin_modificar_prod', methods=['GET','POST'], defaults={'id':None})
@productos_bp.route('/admin_modificar_prod/<int:id>', methods=['GET','POST'] )
def admin_modificar_prod(id):
    idproducto = id 
    mensaje=''
    iduservet = session['iduservet']
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    form_prod = ModificarProducto()
    if request.method == 'GET':
        datos = Productos.query.filter_by(idProducto=idproducto).first()
        return render_template("app/admin_modificar_prod.html",form_prod=form_prod , datos=datos)
    if form_prod.validate_on_submit():
        idprod = form_prod.idproducto.data 
        #nombre = form_prod.nombre_producto.data 
        descripcion = form_prod.descripcion_producto.data 
        precio = form_prod.precio_producto.data 
        #Extraer Producto para actualizar.
        producto = Productos.query.filter_by(idProducto=idprod).filter_by(idvet=idvet).first()
        #Validar si producto pertenece a Veterinaria.
        if producto is None:
            mensaje='Alerta Usted No tiene los permisos para Modificar este Producto'
            flash(mensaje)
            return redirect(url_for('productos_bp.admin_productos'))
        try:
            producto.descripcion = descripcion
            producto.precio = precio
            db.session.commit()
            mensaje='Producto Modificado'
            flash(mensaje)
            return redirect(url_for('productos_bp.admin_productos'))
        except exc.SQLAlchemyError as e:
            mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
            flash(mensaje)
            return redirect(url_for('productos_bp.admin_productos'))
   
    

@productos_bp.route('/admin_aumentar_stock', methods=['GET','POST'], defaults={'id':None})
@productos_bp.route('/admin_aumentar_stock/<int:id>', methods=['GET','POST'] )
def admin_aumentar_stock(id):
    idproducto = id 
    mensaje=''
    iduservet = session['iduservet']
    idvet = session['vet_id']
    nombre_usuario = session['nombre']
    form_stock = StockForm()
    if request.method == 'GET':
        datos = Productos.query.filter_by(idProducto=idproducto).first()
        return render_template("app/aumentar_stock.html",form_stock=form_stock , datos=datos)
    if form_stock.validate_on_submit():
        idprod = form_stock.idproducto.data
        cant = form_stock.aumento.data
        #Validar si producto pertenece a veterinaria.
        validar = Productos.query.filter_by(idProducto=idprod).filter_by(idvet=idvet).first()
        if validar is None:
            mensaje='Alerta Usted No tiene los permisos para Modificar este Producto'
            flash(mensaje)
            return redirect(url_for('productos_bp.admin_productos'))
        try:
            #Si Pertenece Agregar la Cantidad al Producto.
            validar.stock = validar.stock + cant
            #Agregar el Registro al Kardex
            nuevo_kardex = Kardex(None,'Ingreso',nombre_usuario,validar.nombre,cant,0,idvet,None,None)
            db.session.add(nuevo_kardex)
            db.session.commit()
            mensaje='Se agrego ' + str(cant) + ' de Stock al producto ' + str(validar.idProducto)
            flash(mensaje)
            return redirect(url_for('productos_bp.admin_productos'))
        except exc.SQLAlchemyError as e:
            mensaje = "Error : " + str(e._sql_message) + "Reintente o Consulte con Soporte" 
            flash(mensaje)
            return redirect(url_for('productos_bp.admin_productos'))
        return "test2"
    return "test"

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