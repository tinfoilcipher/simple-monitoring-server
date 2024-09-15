# Simple Monitoring Tool

A simple monitoring tool that will periodically check for IP connectivity using ICMP (ping) and HTTP connectivity to web services using Python's requests library. Logs are printed to a simple web page and alerts are sent to a named email address via SMTP. This application is designed to be as straight forward as possible and provide basic monitoring functionality to a very small office or homelab where the costs of setting up a large monitoring infrastructure are too high or otherwise not attractive.

## Running

Configure variables in vars.yaml and run docker.

```bash
#--Backend
docker run -e REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt" -e VARFILE_PATH="/data/vars.yaml" -v /tmp:/tmp -v ${PWD}:/data -v /etc/ssl/certs:/etc/ssl/certs  monitor_backend:1

#--Frontend
docker run -e VARFILE_PATH="/data/vars.yaml" -v /tmp:/tmp -v ${PWD}:/data -p 8081:8081 monitor_frontend:1
```

## Input

All input is via `vars.yaml`. Spec below:

|-------------------------|------------------------------------------------------------------------------------|
| Variable                | Type      | Required | Description                                                 |
|-------------------------|-----------|----------|-------------------------------------------------------------|
| polling_interval        | string    | Y        | Interval in seconds to run connectivity tests               |
| webserver.ip            | string    | Y        | IP for frontend webserver                                   |
| webserver.port          | string    | Y        | TCP port for frontend webserver                             |
| webserver.event_count   | int       | Y        | Number of most recent events to display in frontend         |
| alerting.enabled        | bool      | Y        | Alerting enabled                                            |
| alerting.server         | string    | N        | Alerting SMTP server address                                |
| alerting.recipient      | string    | N        | Alerting SMTP recipient                                     |
| alerting.sender         | string    | N        | Alerting SMTP sender                                        |
| logging.file_path       | string    | Y        | File path for log                                           |
| logging.level           | string    | Y        | Logging level                                               |
| logging.stream_level    | string    | Y        | Logging level for STDOUT, use when running interactively    |
| ip.subnets              | list      | N        | List of IP subnets in CIDR notation                         |
| ip.hosts                | dict      | N        | Dictionary of IP hosts. See example below                   |
| http.hosts              | dict      | N        | Dictionary of HTTP hosts. See example below                 |

## Example Variable File Configuration

- See [Configuration Examples](_example)
