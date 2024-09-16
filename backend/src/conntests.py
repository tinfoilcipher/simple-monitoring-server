import subprocess
from sys import stdout
from contextlib import redirect_stdout
from netaddr import IPNetwork
from requests import get, exceptions
from time import sleep
from logger import log_writer
from alerter import email_alerter

#--Ping Testing
def ping_test(hostname,
              ip):

    try:
        #--Catch the results of a ping. The stderr modification is needed to supress legit errors on the console so they don't noisy things up on a dead host
        subprocess.check_output(["ping", "-c", "1", ip], stderr=subprocess.STDOUT)
        return hostname + " (" + ip + ") is online"
    except subprocess.CalledProcessError:
        return hostname + " (" + ip + ") is offline or unreachable"

#--HTTP Request Testing
def http_test(hostname,
              endpoint):

    response = get('https://' + hostname + "." + endpoint)
    try:
        response.raise_for_status()
        return hostname + " is online: " + str(response.status_code)
    except Exception as error:
        return hostname + " returned an HTTP error: " + str(error) + ". Status Code: " + str(response.status_code)

#--Wraps the above two functions, shouldn't this whole thing be a class? Revisit when you level up!
def connection_tester(polling_interval,
                      monitor_config,
                      alerter_config,
                      logger_config
                      ):
    
    #--Strict variable Extraction, here be dragons
    if "ip" in monitor_config.keys():
        if "hosts" in monitor_config["ip"].keys():
            ip_hosts = monitor_config["ip"]["hosts"]
        else:
            ip_hosts = None
        if "subnets" in monitor_config["ip"].keys():
            ip_subnets = monitor_config["ip"]["subnets"]
        else:
            ip_subnets = None
    else:
        ip_hosts = None
        ip_subnets = None

    if "http" in monitor_config.keys():
        if "hosts" in monitor_config["http"].keys():
            http_hosts = monitor_config["http"]["hosts"]
        else:
            http_hosts = None
    else:
        http_hosts = None

    #--Main monitoring routine routines
    while True:
        responses = []
        alerts = []
        #--IP Subnet
        if ip_subnets is not None:
            for subnet in ip_subnets:
                for ip in IPNetwork(subnet).iter_hosts():
                    ip = str(ip) #--Need to explicitly convert to a string to work with subprocess
                    response = ping_test("Remote Host", ip)
                    log_writer(response, logger_config)
                    responses.append(response)
        else:
            log_writer("No Subnets Defined. Skipping Subnet Checks", logger_config)

        #--IP Host Test
        if ip_hosts is not None:
            for key, value in ip_hosts.items():
                response = ping_test(value["hostname"],
                                    value["ip_address"])
                log_writer(response, logger_config)
                responses.append(response)
        else:
            log_writer("No IP Hosts Defined. Skipping IP Host Checks", logger_config)

        #--HTTP Host Test
        if http_hosts is not None:
            for key, value in http_hosts.items():
                response = http_test(value["hostname"],
                                    value["endpoint"])
                log_writer(response, logger_config)
                responses.append(response)
        else:
            log_writer("No HTTP Hosts Defined. Skipping IP Service Checks", logger_config)

        #--Send any outages to the alerter and loop
        for error in responses:
            if "online" not in error:
                alerts.append(error)

        if not len(alerts) == 0:
            email_alerter(alerts, alerter_config, logger_config)
        sleep(polling_interval)
