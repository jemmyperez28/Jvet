from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from models import Suscripcion, Vet , Vendedor , Uservet , PagoVendedor , HistorialPagovendedor ,ttt as T
from sqlalchemy import exc , desc , func
from forms import VendedorForm , ForgotPassword2 , LoginSuper
from funciones import encriptar
super_vp = Blueprint('super_vp',__name__)

@super_vp.route('/ttt/<nom>', methods=['GET','POST'])
def ttt(nom):
    sec = nom 
    if sec == "revive_the_soul":
        log_vp = LoginSuper()
        return (render_template("/app/tttlog.html",log_vp=log_vp))

@super_vp.route('/ttt/log', methods=['POST'])
def log():
    if request.method == "POST":
        user = request.form["user"]
        pass1 = request.form["pass1"]
        pass2 = request.form["pass2"]
        data = T.query.first()
        print(user)
        print(pass1)
        print(pass2)
        if data.user == user:
            if data.pass1 == encriptar(pass1):
                if data.pass2 == encriptar(pass2):
                    return render_template("/app/super_template.html")
    return "404"
        



    
