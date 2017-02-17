import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from oauth2client import client, crypt
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

# DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')
DATABASE_URL = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

CLIENT_ID = "22643870492-3k4q6eqkdunpp447em29su6e7b7te235.apps.googleusercontent.com"

pst = pytz.timezone('America/Los_Angeles')
utc = pytz.utc
TIME_WINDOW= 1
DIFF = timedelta(minutes=TIME_WINDOW)

WEEKS = {
  0: '2017-01-23',
  1: '2017-01-30',
  2: '2017-02-06',
  3: '2017-02-13',
  4: '2017-02-20',
  5: '2017-02-27',
  6: '2017-03-06',
  7: '2017-03-13',
  8: '2017-03-20',
  9: '2017-03-27',
  10: '2017-04-03',
  11: '2017-04-10',
  12: '2017-04-17',
  13: '2017-04-24',
  14: '2017-05-01',
}

PEOPLE = {
  "s.abdullah@berkeley.edu": "Suhani Abdullah",
  "kabellaneda@berkeley.edu": "Kendra Abellaneda",
  "sunnya97@berkeley.edu": "Sankalp Aggarwal",
  "jimiajayi@berkeley.edu": "Jimi Ajayi",
  "yankunda@berkeley.edu": "Yvette Ankunda",
  "dakshbhatia@berkeley.edu": "Daksh Bhatia",
  "scherny@berkeley.edu": "Sabrina Cherny",
  "adichopra@berkeley.edu": "Aditya Chopra",
  "natalie.chow@berkeley.edu": "Natalie Chow",
  "jenniferdai@berkeley.edu": "Jennifer Dai",
  "kdhillon@berkeley.edu": "Karan Dhillon",
  "cyding@berkeley.edu": "Charles Ding",
  "adiprinzio@berkeley.edu": "Anthony Diprinzio",
  "lehrlich@berkeley.edu": "Liam Ehrlich",
  "jonathan.epstein@berkeley.edu": "Jonathan Epstein",
  "irishman@berkeley.edu": "Brennan Fahselt",
  "arnavgautam@berkeley.edu": "Arnav Gautam",
  "muditg@berkeley.edu": "Mudit Goyal",
  "tylerheintz@berkeley.edu": "Tyler Heintz",
  "adithya.iyengar@berkeley.edu": "Adithya Iyengar",
  "bajue@berkeley.edu": "Brian Jue",
  "skang@berkeley.edu": "Sungwon Kang",
  "parisa.khorram@berkeley.edu": "Parisa Khorram",
  "danielakim@berkeley.edu": "Daniela Kim",
  "jenniferkirby@berkeley.edu": "Jennifer Kirby",
  "ronenkirsh@berkeley.edu": "Ronen Kirsh",
  "koladyr@berkeley.edu": "Rishi Kolady",
  "nkrishnan@berkeley.edu": "Nikhil Krishnan",
  "anushri.kumar@berkeley.edu": "Anushri Kumar",
  "katarinalee@berkeley.edu": "Katarina Lee",
  "federicoli@berkeley.edu": "Federico Li",
  "tliwanag@berkeley.edu": "Therese Liwanag",
  "rileymangubat@berkeley.edu": "Riley Mangubat",
  "smann@berkeley.edu": "Sergey Mann",
  "dmedora@berkeley.edu": "Daryus Medora",
  "brianemickel@berkeley.edu": "Brian Mickel",
  "brian.nguyen@berkeley.edu": "Brian Nguyen",
  "petikyannelly@berkeley.edu": "Nelli Petikyan",
  "sanjay_raavi@berkeley.edu": "Sanjay Raavi",
  "rohit.rajkumar@berkeley.edu": "Rohit Rajkumar",
  "arakeman@berkeley.edu": "Alexander Rakeman",
  "evansheng112@berkeley.edu": "Evan Sheng",
  "robert359@berkeley.edu": "Robert Spragg",
  "csturgill@berkeley.edu": "Derek Sturgill",
  "iris.sun@berkeley.edu": "(Iris) Dingyuan Sun",
  "kthvar@berkeley.edu": "Keshav Thvar",
  "nicoletsai@berkeley.edu": "Nicole Tsai",
  "jessiewang3@berkeley.edu": "Jessie Wang",
  "NEEDS EMAIL": "William Wang",
  "thomas.warloe@berkeley.edu": "Thomas Warloe",
  "NEEDS EMAIL": "Serena Wu",
  "kenny.hyun@berkeley.edu": "Kenny Yoo",
  "carolzhang@berkeley.edu": "Carol Zhang",
  "zhangzhao@berkeley.edu": "Zhao Zhang",
  "NEEDS EMAIL": "Zhe Zhang"
}

# Including ME in the admin list for testing, remove before final!
ADMIN = [
  "jdong@berkeley.edu",
  "surinagulati@berkeley.edu",
  "s.t@berkeley.edu",
  "koladyr@berkeley.edu"
]

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
      time = datetime.now()
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
  for u in check_ins:
    aware = utc.localize(u.time)
    local = aware.astimezone(pst)
    u.time = local
  return render_template('all_entries.html', checkins=check_ins)


@app.route('/week-<number>', methods=['GET'])
def week_check(number):
    date = WEEKS[int(number)]
    check_ins = CheckIn.query.all()
    weekly = {}
    temp_here = []
    here  = []
    absent = []
    time1 = None
    time2 = None
    for u in check_ins:
      aware = utc.localize(u.time)
      local = aware.astimezone(pst)
      u.time = local

      if str(u.time.date()) == date and "Etcheverry Hall" in u.location:
        if u.email in ADMIN:
          if time1 is None:
            time1 = u.time.time()
          else:
            time2 = u.time.time()
        if u.email not in weekly:
          condense = {
            "name": u.name,
            "email": u.email,
            "time1": u.time.time(),
            "time2": None
          }

          weekly[u.email] = condense
        else:
          weekly[u.email]["time2"] = u.time.time()

    for email in weekly:
      person = weekly[email]
      if person["time2"] is not None:
        person_first = person["time1"]
        if time1 is not None and time1 + DIFF > person_first and time1 - DIFF < person_first:
          person_second = person["time2"]
          if time2 is not None and time2 + DIFF > person_second and time2 - DIFF < person_second:
            temp_here.append(email)

    for email in PEOPLE:
      if email in temp_here:
        here.append((PEOPLE[email], email))
      else:
        absent.append((PEOPLE[email], email))

    return render_template("weekly.html", week=number, here=here, absent=absent)


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
