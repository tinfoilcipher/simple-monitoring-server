from yaml import safe_load
from threading import Thread
from conntests import connection_tester
from time import sleep

#--Variable Loading
with open('vars.yaml', 'r') as varfile:
     vars = safe_load(varfile)
     polling_interval = vars["polling_interval"]
     ip_config = vars["ip"]
     http_config = vars["http"]
     alerter_config = vars["alerting"]

#--Application startup
if __name__ == "__main__":
     connection_tester(
          polling_interval,
          ip_config,
          http_config,
          alerter_config
          )
