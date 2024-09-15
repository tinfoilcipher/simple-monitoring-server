# Simple Monitoring Tool

A simple monitoring tool that will periodically check for IP connectivity using ICMP (ping) and HTTP connectivity to web services using Python's requests library. Logs are printed to a simple web page and alerts are sent to a named email address via SMTP. This application is designed to be as straight forward as possible and provide basic monitoring functionality to a very small office or homelab where the costs of setting up a large monitoring infrastructure are too high or otherwise not attractive.

## Running

### Docker

```bash
export VARFILE_PATH="/data/vars.yaml"
docker-compose up -f compose.yaml
```

### Local Dev

```bash
export VARFILE_PATH="vars.yaml"
python backend/src/app.py
python frontend/src/app.py
```

## Input

### Environment Variables

| Variable            | Type      | Required | Description                                                                     |
|---------------------|-----------|----------|---------------------------------------------------------------------------------|
| VARFILE_PATH        | string    | Y        | Path to vars.yaml input file                                                    |
| REQUESTS_CA_BUNDLE  | string    | N        | Path to private CA file. Needed if testing HTTP services signed by a private CA |

### YAML Variables

All input is via `vars.yaml`. Spec below:

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

## Use With a Private CA

Before Python's requests library will trust your private CA it will first need to know about it's CA Certificate. Since disabling TLS validation is a bad thing to do, take a few seconds to do it properly. Assuming your OS already has your CA's certs installed...

```bash
export REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
```

This is the path for Ubuntu, locations differ on other distros and in Windows. This variable will inform the application where to look for your systems CA certs. Once this is set, add a line to the `compose.yaml` under `services.backend.environment.volumes` to mount your systems CA certs in to the application, I.E.:

```yaml
services: 
  ...
    volumes:
      - /tmp:/tmp
      - ./:/data
      - /etc/ssl/certs:/etc/ssl/certs #--Add this line
    ...
```

The app can then be launched as usual.
