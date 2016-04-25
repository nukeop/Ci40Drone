import logging,logging.handlers, random, time

from flask import Flask, render_template, flash, request, session

from dronestatus import DroneStatus
from DroneMessages import DroneMessages

app = Flask(__name__)
app.secret_key = "32730bc1b37f672746fcc388a5d117f3"

ds = DroneStatus()
dm = DroneMessages(app)

droneoutput = []

def setup_logger():
    handler = logging.handlers.RotatingFileHandler("serverlog.log", mode='a', maxBytes=1024*512, backupCount=3)
    formatter = logging.Formatter("[%(process)d] [%(asctime)s] [%(levelname)s] - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

def load_log_lines():
    return open("serverlog.log", 'r').readlines()

@app.route('/')
def index(title="Drone Home Page", drone_status=None, loadtime=None):
    loadstart = time.time()
    
    drone_status = ds.status
    
    loadtime = round(time.time()-loadstart, 3)
    return render_template("index.html", title=title, drone_status=drone_status, loadtime=loadtime)

@app.route('/startup', methods=['POST', 'GET'])
def startup(title="Drone Startup Page", drone_status=None, loadtime=None):
    loadstart = time.time()
    droneoutput = ""

    if request.method == 'POST':
        if not dm.connected:
            ports = filter(None, [request.form['port1'], request.form['port2'], request.form['port3'], request.form['port4']])
            dm.connect(ports)
            session['port1'] = ports[0]
            session['port2'] = ports[1]
            session['port3'] = ports[2]
            session['port4'] = ports[3]
    elif request.method == 'GET':
        try:
            command = request.args['command']
            if command == "kill":
                dm.send_kill()
            elif command == "increase":
                dm.increase_throttle(5)
            elif command == "decrease":
                dm.decrease_throttle(5)
            elif command == "set":
                dm.set_throttle(request.args['amount'])
        except KeyError:
            pass

    droneoutput = reversed(load_log_lines())
        
    drone_status = ds.status
    loadtime = round(time.time()-loadstart, 3)
    return render_template("startup.html", title=title, drone_status=drone_status, loadtime=loadtime, connected=dm.connected, droneoutput=droneoutput)

if __name__ == '__main__':
    setup_logger()
    app.run(host="0.0.0.0", debug=True)
