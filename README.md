# Simple Monitoring Tool

A simple monitoring tool that will periodically check for IP connectivity using ICMP (ping) and HTTP connectivity to web services using Python's requests library. Logs are printed to a simple web page and alerts are sent to a named email address via SMTP. This application is designed to be as straight forward as possible and provide basic monitoring functionality to a very small office or homelab where the costs of setting up a large monitoring infrastructure are too high or otherwise not attractive.

## Running

### Docker

```bash
export VARFILE_PATH="/data/vars.yaml"
export SERVER_HOSTNAME="monitoring.mydomain.com"
docker-compose up -f compose.yaml
```

Access at `http://localhost`.

### Local Dev

```bash
export VARFILE_PATH="vars.yaml"
python backend/src/app.py
python frontend/src/app.py
```

Access at `http://localhost:8081`.

## Input

### Environment Variables

| Variable            | Type      | Required | Description                                                                     |
|---------------------|-----------|----------|---------------------------------------------------------------------------------|
| VARFILE_PATH        | string    | Y        | Path to vars.yaml input file                                                    |
| SERVER_HOSTNAME     | string    | Y        | HTTP hostname for webserver. Defaults to `localhost`                            |
| REQUESTS_CA_BUNDLE  | string    | N        | Path to private CA file. Needed if testing HTTP services signed by a private CA |

### YAML Variables

All input is via `vars.yaml`. Spec below:

| Variable                | Type      | Required | Description                                                 |
|-------------------------|-----------|----------|-------------------------------------------------------------|
| polling_interval        | string    | Y        | Interval in seconds to run connectivity tests               |
| frontend_count          | int       | Y        | Number of most recent events to display in frontend         |
| alerting.enabled        | bool      | Y        | Alerting enabled                                            |
| alerting.server         | string    | N        | Alerting SMTP server address                                |
| alerting.recipient      | string    | N        | Alerting SMTP recipient                                     |
| alerting.sender         | string    | N        | Alerting SMTP sender                                        |
| logging.file_path       | string    | Y        | File path for log                                           |
| logging.level           | string    | Y        | Logging level                                               |
| logging.stream_level    | string    | Y        | Logging level for STDOUT, use when running interactively    |
| monitors.ip.subnets     | list      | N        | List of IP subnets in CIDR notation                         |
| monitors.ip.hosts       | dict      | N        | Dictionary of IP hosts. See example below                   |
| monitors.http.hosts     | dict      | N        | Dictionary of HTTP hosts. See example below                 |

## Example Variable File Configuration

- See [Configuration Examples](_example)

## Monitoring HTTPS Services Signed By a Private CA

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
      - /etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro #--Add this line
    ...
```

The app can then be launched as usual.

## Configuring NGINX To Use HTTPS

Generate your own TLS certificate and key and update the `nginx.conf` and `compose.yaml` files as below:

```conf
#--nginx.conf
upstream frontend {
    server frontend:8081;
}

server {
    listen 443 ssl;

    location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
    }
    ssl_certificate     /etc/ssl/certs/your_certificate.crt;
    ssl_certificate_key /etc/ssl/private/your_key.key;
}
```

```yaml
#--docker-compose.yaml
  ...
  proxy:
    depends_on:
      - frontend
    image: nginx
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - /etc/ssl/certs/your_certificate.crt:/etc/ssl/certs/your_certificate.crt:ro
      - /etc/ssl/private/your_key.key:/etc/ssl/private/your_key.key:ro
  ...
```

Ensure to `export SERVER_HOSTNAME=myserver.domain.com` before running the application. The server should be acessible at `https://$SERVER_HOSTNAME` on launch.
