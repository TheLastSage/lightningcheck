import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from oauth2client import client, crypt

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

  def __init__(self, name, email, location):
    self.name = name
    self.email = email
    self.location = location

  def __repr__(self):
    return '<Name %r>' % self.location


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
    location = request.json ['location']
    token = request.json['idtoken']

    try:
      idinfo = client.verify_id_token(token, CLIENT_ID)

      # if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
          # raise crypt.AppIdentityError("Wrong issuer.")

      # If auth request is from a G Suite domain:
      #if idinfo['hd'] != GSUITE_DOMAIN_NAME:
      #    raise crypt.AppIdentityError("Wrong hosted domain.")

    #   name = idinfo['name']
    #   email = idinfo['email']

      return 'worked', 200
    except crypt.AppIdentityError:
      # Invalid token
      return 'failed', 200

    # u = User(request.form['name'], request.form['email'], request.form['location'])
    # u = User(request.json['name'], request.json['email'], request.json['location'])
    # u = User("test" , "email", "please")
    # db.session.add(u)
    # db.session.commit()
    # return redirect(url_for('index'))
    return '', 204

if __name__ == '__main__':
  # db.create_all()
  # db.session.commit()
  # u1 = User('test', 'email', 'testloc')
  # db.session.add(u1)
  # db.session.commit()

  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
