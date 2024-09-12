from yaml import safe_load
from flask import Flask, render_template
from waitress import serve

#--Variable handling
with open('vars.yaml', 'r') as varfile:
     vars = safe_load(varfile)
     config = vars["webserver"]

app = Flask(__name__)

@app.route('/') 
def index():
     try:
          with open('monitor.log', 'r') as logfile:
               log_print = []
               log = logfile.read().splitlines()
               log_end = len(log)
               log_start = (log_end - config["event_count"])
               for log_line in reversed(list(log[log_start:log_end])):
                    log_print.append(log_line)
          return render_template('index.html', line_count=config["event_count"], log_print=log_print)
     except:
          return "Fatal Error. Probably an input file is missing!"

if __name__ == "__main__":
     print(f"Starting Monitor...")
     serve(app, host=config["ip"], port=config["port"])
