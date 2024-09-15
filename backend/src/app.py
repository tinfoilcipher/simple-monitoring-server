from yaml import safe_load
from os import environ
from logger import log_writer
from threading import Thread
from conntests import connection_tester
from time import sleep

#--Variable Loading
try:
     with open(environ['VARFILE_PATH'], 'r') as varfile:
          vars = safe_load(varfile)
          polling_interval = vars["polling_interval"]
          ip_config = vars["ip"]
          http_config = vars["http"]
          alerter_config = vars["alerting"]
          logger_config = vars["logging"]

     print(f"Starting Monitoring Backend")

     if __name__ == "__main__":
          connection_tester(
               polling_interval,
               ip_config,
               http_config,
               alerter_config,
               logger_config
               )
          
except KeyError:
     print(f"Input Error. Probably missing variable input file, did you define VARFILE_PATH?")
except Exception as error:
     #--General start error
     print("The application has failed to start, Oh No! Reason:", error)
