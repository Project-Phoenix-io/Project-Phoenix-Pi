from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_restful import Resource, Api
from datetime import timedelta
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)

pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

@app.route('/')
def index():
  if 'password' in session:
    return render_template('index.html')
  else:
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    if int(request.form['password']) == app.config['PASSWORD']:
      session['password'] = int(request.form['password'])
      return redirect(url_for('index'))
    else:
      return redirect(url_for('login'))
  
  return render_template('login.html')

@app.route('/logout')
def logout():
  session.pop('password', None)
  return redirect(url_for('index'))

class apiLogin(Resource):
  def post(self):
    if int(request.form['password']) == app.config['PASSWORD']:
      return 'ok', 200
    else:
      return 'not ok', 401

class apiExtinguish(Resource):
  def get(self):
    GPIO.output(pin, True)
    return 'ok', 200

class apiShutdown(Resource):
  def get(self):
    GPIO.output(pin, False)
    return 'ok', 200

class apiPulse(Resource):
  def post(self):
    print(request.form)
    for i in range(0, int(request.form['iterations'])):
        GPIO.output(pin, True)
        print('Extinguishing')
        time.sleep(int(request.form['timeOn']))
        GPIO.output(pin, False)
        print('Waiting')
        time.sleep(int(request.form['timeOff']))
    return 'ok', 200

class apiFindMe(Resource):
  def get(self):
    return 'ok', 200


api.add_resource(apiFindMe, '/api')
api.add_resource(apiLogin, '/api/login')
api.add_resource(apiExtinguish, '/api/extinguish')
api.add_resource(apiShutdown, '/api/shutdown')
api.add_resource(apiPulse, '/api/pulse')

if __name__ == "__main__":
  app.run(debug = True, host = '0.0.0.0')
  
GPIO.cleanup()