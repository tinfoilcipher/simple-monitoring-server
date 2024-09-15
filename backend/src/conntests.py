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
    except exceptions.HTTPError:
        return hostname + " returned an HTTP error: " + str(response.status_code)
    except exceptions.ConnectionError:
        return hostname + " returned a connection error: " + str(response.status_code)
    except exceptions.Timeout:
        return hostname + " returned a timeout error: " + str(response.status_code)
    except exceptions.RequestException:
        return "OH NO! " + hostname + " has an unclear HTTP error, solar flares?: " + str(response.status_code)

#--Wraps the above two functions, shouldn't this whole thing be a class? Revisit when you level up!
def connection_tester(polling_interval,
                      ip_config,
                      http_config,
                      alerter_config,
                      logger_config
                      ):

    while True:
        responses = []
        alerts = []
        #--IP Subnet
        try:
            ip_config["subnets"]
            for subnet in ip_config["subnets"]:
                
                for ip in IPNetwork(subnet).iter_hosts():
                    ip = str(ip) #--Need to explicitly convert to a string to work with subprocess
                    response = ping_test("Remote Host", ip)
                    log_writer(response, logger_config)
                    responses.append(response)
        except:
            log_writer("ip.subnets Is Not Defined. Skipping Full Subnet Test.", logger_config)

        #--IP Host Test
        try:
            ip_config["hosts"]
            for key, value in ip_config["hosts"].items():
                response = ping_test(value["hostname"],
                                    value["ip_address"])
                log_writer(response, logger_config)
                responses.append(response)
        except:
            log_writer("ip.hosts Is Not Defined. Skipping Host Tests.", logger_config)

        #--HTTP Host Test
        try:
            http_config["hosts"]
            for key, value in http_config["hosts"].items():
                response = http_test(value["hostname"],
                                    value["endpoint"])
                log_writer(response, logger_config)
                responses.append(response)
        except:
            log_writer("http.hosts is Not Defined. Skipping Host Tests.", logger_config)

        #--Send any outages to the alerter and loop
        for error in responses:
            if "online" not in error:
                alerts.append(error)

        if not len(alerts) == 0:
            email_alerter(alerts, alerter_config)

        sleep(polling_interval)
