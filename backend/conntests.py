import subprocess
from sys import stdout
from contextlib import redirect_stdout
from requests import get, exceptions
from time import sleep
from logwriter import log_writer
from alerter import email_alerter

#--Ping Testing
def ping_test(hostname,
              ip_host,
              ip_prefix,
              enabled):
    
    if enabled is True:
        ip = ip_prefix + ip_host
        try:
            #--Catch the results of a ping. The stderr modification is needed to supress legit errors on the console so they don't noisy things up on a dead host
            subprocess.check_output(["ping", "-c", "1", ip], stderr=subprocess.STDOUT)
            return hostname + " (" + ip + ") is online"
        except subprocess.CalledProcessError:
            return hostname + " (" + ip + ") is offline or unreachable"

#--HTTP Request Testing
def http_test(hostname,
              domain,
              endpoint,
              enabled):
    
    if enabled is True:
        response = get('https://' + hostname + "." + domain + endpoint)
        try:
            response.raise_for_status()
            return hostname + "." + domain + " is online: " + str(response.status_code)
        except exceptions.HTTPError:
            return hostname + "." + domain + " returned an HTTP error: " + str(response.status_code)
        except exceptions.ConnectionError:
            return hostname + "." + domain + " returned a connection error: " + str(response.status_code)
        except exceptions.Timeout:
            return hostname + "." + domain + " returned a timeout: " + str(response.status_code)
        except exceptions.RequestException:
            return "OH NO! " + hostname + "." + domain + " is broken in some inexplicable way: " + str(response.status_code)

#--Wraps the above two functions, shouldn't this whole thing be a class?
#def connection_tester(polling_interval, ip_hosts, ip_prefix, ip_enabled, http_hosts, http_domain, http_enabled):
def connection_tester(polling_interval,
                      ip_config,
                      http_config,
                      mailer_config,
                      ):

    while True:
        responses = []
        alerts = []
        for key, value in ip_config["hosts"].items():
            response = ping_test(value["hostname"],
                                 value["ip_host"],
                                 ip_config["prefix"],
                                 ip_config["enabled"])
            log_writer(response)
            responses.append(response)

        for key, value in http_config["hosts"].items():
            response = http_test(value["hostname"],
                                 http_config["domain"],
                                 value["endpoint"],
                                 http_config["enabled"])
            log_writer(response)
            responses.append(response)

        #--Send any outages to the alerter and loop
        for error in responses:
            if "online" not in error:
                alerts.append(error)

        if not len(alerts) == 0:
            email_alerter(alerts, mailer_config)

        sleep(polling_interval)
