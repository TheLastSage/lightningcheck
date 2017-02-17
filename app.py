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


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))
  location = db.Column(db.String(100))
  # time = db.Column(db.DateTime)

  def __init__(self, name, email, location):
    self.name = name
    self.email = email
    self.location = location

  def __repr__(self):
    return '<Name: ' + self.name + ', Email: ' + self.email + ', Location: ' + self.location + '>'


@app.route('/', methods=['GET'])
def index():
  users = User.query.all()
  # return render_template('index.html', users=users)
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

      u = User(name, email, location)
      db.session.add(u)
      db.session.commit()


      return "Name: " + name + ", Email: " + email, 200
    except crypt.AppIdentityError:
      # Invalid token
      return "OAuth Identity Error", 200

    return redirect(url_for('index'))

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
