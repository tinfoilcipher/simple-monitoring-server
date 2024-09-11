from yaml import safe_load
from flask import Flask
from waitress import serve

#--Variable handling
with open('vars.yaml', 'r') as f:
     vars = safe_load(f)
     config = vars["webserver"]

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
     serve(app, host=config["ip"], port=config["port"])
