import hashlib
from functools import wraps 
from flask import request , redirect , session

def encriptar(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def super_required(funcion):
    @wraps(funcion)
    def wrapper(*args,**kwargs):
        nivel = session['tipo_uservet'] 
        if nivel: 
            if nivel == 'super':
                return funcion(*args,**kwargs)
            else:
                return redirect('/login_usuario')
        else: 
            return redirect('/login_usuario')
    return wrapper 

def admin_required(funcion):
    @wraps(funcion)
    def wrapper(*args,**kwargs):
        nivel = session['tipo_uservet'] 
        if nivel: 
            if nivel == 'admin':
                return funcion(*args,**kwargs)
            else:
                return redirect('/login_usuario')
        else: 
            return redirect('/login_usuario')
    return wrapper 

def vend_required(funcion):
    @wraps(funcion)
    def wrapper(*args,**kwargs):
        nivel = session['tipo_uservet'] 
        if nivel: 
            if nivel == 'vendedor':
                return funcion(*args,**kwargs)
            else:
                return redirect('/login_usuario')
        else: 
            return redirect('/login_usuario')
    return wrapper 

