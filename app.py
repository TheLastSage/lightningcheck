import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from oauth2client import client, crypt
from datetime import datetime
import pytz

app = Flask(__name__)

# DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')
DATABASE_URL = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

CLIENT_ID = "22643870492-3k4q6eqkdunpp447em29su6e7b7te235.apps.googleusercontent.com"

pst = pytz.timezone('America/Los_Angeles')


class CheckIn(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))
  location = db.Column(db.String(100))
  time = db.Column(db.DateTime)

  def __init__(self, name, email, location, time=None):
    self.name = name
    self.email = email
    self.location = location

    if time is None:
      time = datetime.now(tz=pst)
    self.time = time

  def __repr__(self):
    return '<Name: ' + self.name + ', Email: ' + self.email + ', Location: ' + self.location + ', Time: ' + str(self.time.time()) + '>'


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
  if request.method == 'GET':
    return redirect(url_for('index'))
  elif request.method == 'POST':
    location = request.json['location']
    token = request.json['idtoken']

    try:
      idinfo = client.verify_id_token(token, CLIENT_ID)

      if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
          raise crypt.AppIdentityError("Wrong issuer.")

      if idinfo['aud'] != CLIENT_ID:
          raise crypt.AppIdentityError("Wrong Client.")

      name = idinfo['name']
      email = idinfo['email']

      u = CheckIn(name, email, location)
      db.session.add(u)
      db.session.commit()


      return "Name: " + name + ", Email: " + email, 200
    except crypt.AppIdentityError:
      # Invalid token
      return "OAuth Identity Error", 200

    return redirect(url_for('index'))

@app.route('/all', methods=['GET'])
def all():
  check_ins = CheckIn.query.all()
  return render_template('all_entries.html', checkins=check_ins)


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
