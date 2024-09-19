"""A simple web interface to read a monitoring logfile and display it in HTML"""

from os import environ
from yaml import safe_load
from flask import Flask, render_template
from waitress import serve

#--Variable handling
with open(environ['VARFILE_PATH'], 'r', encoding="utf-8") as varfile:
    input_vars = safe_load(varfile)
    line_count = input_vars["frontend_count"]
    logger_config = input_vars["logging"]

print("Starting Monitoring Frontend")

app = Flask(__name__)

@app.route('/')
def index():
    """Launches flask and serves application via waitress.

    Reverses order of log file and displays the latest amount of logs as
    specified in frontend_count.

    Returns:
        error_msg (str): All purpose failure error message
    """
    try:
        with open(logger_config["file_path"], 'r', encoding="utf-8") as logfile:
            log_print = []
            log = logfile.read().splitlines()
            log_end = len(log)
            log_start = log_end - line_count
            for log_line in reversed(list(log[log_start:log_end])):
                log_print.append(log_line)
        return render_template('index.html', line_count=line_count, log_print=log_print)
    except Exception as error:
        error_msg = "Fatal Error. Probably an input file is missing! Did you set VARFILE_PATH?. Error:" + error
        return error_msg

if __name__ == "__main__":
    print("Starting WSGI...")
    serve(app, host="0.0.0.0", port="8081")
