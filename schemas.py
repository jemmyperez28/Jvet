from flask_marshmallow import Marshmallow
from models import Uservet
ma = Marshmallow()

class UserVetSchema(ma.Schema):
    class Meta:
        model = Uservet

user_vet_1 = ['dni','email','nombre','apellidos','telefono','tipo_uservet']


        