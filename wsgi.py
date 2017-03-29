from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

user = os.environ["MYSQL_USER"]
passw = os.environ["MYSQL_PASSWORD"]
dbhost = os.environ["MYSQL_SERVICE_HOST"]
dbname = os.environ["MYSQL_DATABASE"]

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + user + ":" + passw +
                                                '@' + dbhost + "/" + dbname
application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)
bootstrap = Bootstrap(application)

class State(db.Model):
  __tablename__ = 'states'
  did = db.Column(db.String(4), primary_key=True)
  timestamp = db.Column(db.String(32), primary_key=True)
  state = db.Column(db.String(16))

  def __init__(self, did, timestamp, state):
    self.did = did
    self.timestamp = timestamp
    self.state = state

  def __refr__(self):
    return '<State %r>' % self.name

@application.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    # Add to the database and display updated values
    state = State(request.json['deviceId'], request.json['timestamp'],
		  request.json['operationalState'])
    db.session.add(state)
    db.session.commit()
    return jsonify({'success': 'state change added'}), 201
  else:
    # Display last 10 updates
    states = State.query.order_by(State.timestamp.desc()).limit(10).all()
    return render_template('index.html', states=states)
    
if __name__ == '__main__':
  application.run(debug=True)
