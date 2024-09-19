"""A simple monitoring tool to check if IP hosts/HTTP services are online
and raise email alerts if they aren't."""

from os import environ
from yaml import safe_load
from conntests import connection_tester

#--Variable Loading
try:
    with open(environ['VARFILE_PATH'], 'r', encoding="utf-8") as varfile:
        input_vars = safe_load(varfile)
        polling_interval = input_vars["polling_interval"]
        monitor_config = input_vars["monitors"]
        alerter_config = input_vars["alerting"]
        logger_config = input_vars["logging"]

    print("Starting Monitoring Backend")

    if __name__ == "__main__":
        connection_tester(
            polling_interval,
            monitor_config,
            alerter_config,
            logger_config
        )

except KeyError:
    print("Input Error. Probably missing or misformatted variable input file, did you define VARFILE_PATH?")
except Exception as error:
    print("The application has failed to start, Oh No! Reason:", error)
