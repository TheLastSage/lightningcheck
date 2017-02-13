import os

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))
  location = db.Column(db.String(100))

  def __init__(self, name, email, location):
    self.name = name
    self.email = email
    self.location = locations


@app.route('/', methods=['GET'])
def index():
  # users = db.session.query(User).all()
  # return render_template('index.html', users=users)
  return render_template('index.html')  


# @app.route('/user', methods=['POST'])
# def user():
#   u = User(request.form['name'], request.form['email'])
#   db.session.add(u)
#   db.session.commit()
#   return redirect(url_for('index'))

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
  if request.method == 'GET':
    return redirect(url_for('index'))
  elif request.method == 'POST':
    u = User(request.args.get('name'), request.args.get('email'), request.args.get('location'))
    # db.session.add(u)
    # db.session.commit()
    # return redirect(url_for('index'))
    return '', 204

if __name__ == '__main__':
  # db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
