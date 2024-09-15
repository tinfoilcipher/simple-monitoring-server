from os import environ
from yaml import safe_load
from flask import Flask, render_template
from waitress import serve

#--Variable handling
with open(environ['VARFILE_PATH'], 'r') as varfile:
     vars = safe_load(varfile)
     wsgi_config = vars["webserver"]
     logger_config = vars["logging"]

print(f"Starting Monitoring Frontend")

app = Flask(__name__)

@app.route('/') 
def index():
     try:
          with open(logger_config["file_path"], 'r') as logfile:
               log_print = []
               log = logfile.read().splitlines()
               log_end = len(log)
               log_start = (log_end - wsgi_config["event_count"])
               for log_line in reversed(list(log[log_start:log_end])):
                    log_print.append(log_line)
          return render_template('index.html', line_count=wsgi_config["event_count"], log_print=log_print)
     except:
          return "Fatal Error. Probably an input file is missing! Did you set VARFILE_PATH and is there a log to read from?"

if __name__ == "__main__":
     print(f"Starting WSGI...")
     serve(app, host=wsgi_config["ip"], port=wsgi_config["port"])
