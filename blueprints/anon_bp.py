from flask import Blueprint , render_template , request , session , redirect , url_for , flash , current_app 
import flask 
from config.db import db 
from models import Vet
from sqlalchemy import exc , desc , func
anon_bp = Blueprint('anon_bp',__name__)

@anon_bp.route('/', methods=['GET','POST'])
def index_anon():
    datos = Vet.query.all()
    return render_template("/app/anon_index.html",datos=datos)

