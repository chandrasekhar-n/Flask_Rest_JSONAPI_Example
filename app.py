from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from marshmallow_jsonapi.flask import Schema
from marshmallow import validate
from marshmallow_jsonapi import fields

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1:3306/test'
app.config['PAGE_SIZE'] = 10
db = SQLAlchemy(app)

class Pulse(db.Model):
    __tablename__ = 'pulse'
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(100),unique=True)
    type = db.Column('type',db.String(10))
    max_rabi_rate = db.Column('max_rabi_rate',db.Integer)
    polar_angle = db.Column('polar_angle',db.DECIMAL)

db.create_all()

PULSE_TYPES = ['Primitive', 'CORPSE', 'Gaussian', 'CinBB', 'CinSK']

class PulseSchema(Schema):
    class Meta:
        type_ = 'pulse'
        self_view = 'pulse_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'pulses_list'

    id = fields.Integer()
    name = fields.Str()
    type = fields.Str(validate=validate.OneOf(PULSE_TYPES))
    max_rabi_rate = fields.Integer(validate=validate.Range(min=0,max=100))
    polar_angle = fields.Decimal(validate = validate.Range(min=0,max=1))
    
class PulseList(ResourceList):
    schema = PulseSchema
    data_layer = {'session': db.session,
                  'model': Pulse}

class PulseDetail(ResourceDetail):
    schema = PulseSchema
    data_layer = {'session': db.session,
                  'model': Pulse
                  }

@app.route("/",methods=['GET'])
def hellow():
    return "hello world"

@app.route("/pulses/download")
def downloadpulses():
    print("downloading pulses")

api = Api(app)
api.route(PulseList,'pulses_list','/pulses')
api.route(PulseDetail,'pulse_detail','/pulses/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)



