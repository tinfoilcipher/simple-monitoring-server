# Madcaplaughs Monitoring Tool

Simple python tool that monitors uptime of IP Hosts and HTTP services, then fires email alerts if one of them goes down.

## Running

```bash
#--Add alias to .bashrc alias pypm="python3 -m pypm"
pip install -r requirements.txt
pypm add backend "python src/backendend/app.py"
pypm add frontend "python src/frontend/app.py"
pypm start backend
pypm start frontend
```
