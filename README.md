# Hetzner DNS Updater

Simple Tool for creating/ updating DNS records with your current IP (v4).

- Basic settings are provided via Docker Environment Variables.
- DNS entries are provided via csv file.
- Status output via console.
- Used service for IP detection: `api.ipify.org`.

## Usage
1. Create API-Token at Hetzner DNS Console.
2. Create a `records.csv` and fill it with your DNS entries.
3. Deploy via Docker.

## Docker Deployment

- Replace `my_path` with the path to your `records.csv`.
- Replace `my_token` with your Hetzner DNS API token.
- Optional: Change Update interval (Defaul: 600 seconds).
- Optional: Change TTL for DNS Entries (Default: 84600).

### Deployment via CLI
```
docker run -v /my_path/records.csv:/records.csv -e api_token=my_token docker.io/elem74/hetzner_dns_updater
```

### Deployment via Compose File
```
services:
    hetzner_dns_updater:
        image: docker.io/elem74/hetzner_dns_updater
        volumes:
            - /my_path/records.csv:/records.csv
        environment:
        - api_token=my_token
        # - update_interval=600 # (optional)
        # - ttl = 84600 # (optional)
```

## Sample records.csv

### Domains
- friendly.sample.dev
- happy.sample.dev
- www.sample.dev

### File Structure
| zone         | type | name     |
| ------------ | ---- | -------- |
| sample.dev | A    | friendly |
| sample.dev | A    | happy    |
| sample.dev | A    | www      |

### Plain-Text CSV
```
zone;type;name
sample.dev;A;www
sample.dev;A;friendly
sample.dev;A;happy
```