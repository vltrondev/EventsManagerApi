from crypt import methods

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



# configurando mi ORM con sqlAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/events'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# creando mi ORM de flask con la libreria de flask_sqlalchemy
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(85), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, event, category, date):
        self.event = event
        self.category = category
        self.date = date

with app.app_context():
    db.create_all()


# creando el schema de mi db
class EventSchema(ma.Schema):
    class Meta:
        fields = ('id', 'event', 'category', 'date')



event_schema = EventSchema()
events_schema = EventSchema(many=True)


# enpoint con metodo POST para recivir los datos del evento
@app.route('/events', methods=['POST'])
def create_event():
    # reciviendo los datos de mi evento
    event = request.json['event']
    category = request.json['category']
    date = request.json['date']

    # agregando y guardando los datos recividos en mi db
    new_event = Events(event, category, date)
    db.session.add(new_event)
    db.session.commit()

    # devolviendo los datos capturados
    return event_schema.jsonify(new_event)



# creando mi endpoint GET para obtener todos los eventos guardados
@app.route('/events', methods=['GET'])
def get_events():
    all_events = Events.query.all()
    result = events_schema.dump(all_events)
    return jsonify(result)



# opcion para obtener los datos individuales
@app.route(f'/events/<id>', methods=['GET'])
def get_event(id):
    event = Events.query.get(id)
    return event_schema.jsonify(event)


# creando mi endpoint para actualizar datos de mis eventos
@app.route('/events/<id>', methods=['PUT'])
def update_event(id):
    events = Events.query.get(id)
    event = request.json['event']
    category = request.json['category']
    date = request.json['date']

    events.event = event
    events.category = category
    events.date = date

    db.session.commit()
    return event_schema.jsonify(events)



#eliminar tareas
@app.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    event = Events.query.get(id)
    db.session.delete(event)
    db.session.commit()

    return event_schema.jsonify(event)

if __name__ == "__main__":
    app.run(debug=True)