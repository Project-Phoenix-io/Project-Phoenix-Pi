from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_restful import Resource, Api
from datetime import timedelta
import RPi.GPIO as GPIO

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, True)
GPIO.cleanup()

@app.route('/')
def index():
  if 'username' in session:
    return render_template('index.html', username=session['username'])
  else:
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
      session['username'] = request.form['username']
      return redirect(url_for('index'))
    else:
      return redirect(url_for('login'))
  
  return render_template('login.html')

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))

class apiLogin(Resource):
  def post(self):
    if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
      print('Login is good ' + request.form['username'] + ':' + app.config['USERNAME'])
      return 'ok', 200
    else:
      return 'not ok', 401

class apiExtinguish(Resource):
  def get(self):
    GPIO.output(15, True)
    return 'ok', 200

class apiShutdown(Resource):
  def get(self):
    GPIO.output(15, False)
    return 'ok', 200

class apiFindMe(Resource):
  def get(self):
    retirm 'ok', 200

api.add_resource(apiLogin, '/api/login')
api.add_resource(apiExtinguish, '/api/extinguish')
api.add_resource(apiShutdown, '/api/shutdown')
api.add_resource(apiFindMe, '/api')

if __name__ == "__main__":
  app.run(debug = True, host = '0.0.0.0')