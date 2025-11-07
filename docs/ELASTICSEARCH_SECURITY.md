# Elasticsearch Security Setup Guide

## Overview

Elasticsearch is now configured with security enabled (`xpack.security.enabled: true`) to support API key creation in Kibana.

## Default Credentials

- **Elasticsearch**:
  - Username: `elastic`
  - Password: `password`
- **Kibana**: Uses service account token (configured automatically)

## Starting Services

```bash
# Set the service token environment variable
export KIBANA_SERVICE_TOKEN="AAEAAWVsYXN0aWMva2liYW5hL215dG9kb2FwcC1raWJhbmEtdG9rZW46MWJVLVJqYnFSdGlERjFnb19FMkIxUQ"

# Start all services
make dev
```

## Service URLs

- **Elasticsearch**: <http://localhost:9200> (requires authentication)
- **Kibana**: <http://localhost:5601> (login with Elastic user)
- **Grafana**: <http://localhost:3000> (admin/admin)
- **Prometheus**: <http://localhost:9090>

## Creating API Keys in Kibana

1. Open <http://localhost:5601> in your browser
2. Login with:
   - Username: `elastic`
   - Password: `password`
3. Navigate to **Stack Management** → **Security** → **API Keys**
4. Click **"Create API key"**
5. Fill in the details:
   - **Name**: Give your API key a descriptive name
   - **Expiration**: Set expiration (optional)
   - **Role descriptors**: Define permissions (optional)
6. Click **"Create API key"**
7. Copy the generated API key and store it securely

## Testing Elasticsearch with Authentication

```bash
# Basic health check
curl -u elastic:password http://localhost:9200/_cat/health

# List indices
curl -u elastic:password http://localhost:9200/_cat/indices

# Using API key (after creation)
curl -H "Authorization: ApiKey YOUR_API_KEY_HERE" http://localhost:9200/_cat/health
```

## Important Security Notes

1. **Change Default Password**: In production, change the default `password` to a stronger one
2. **Service Token**: The Kibana service token is automatically configured
3. **API Keys**: Store API keys securely and rotate them regularly
4. **Network**: Only expose ports that are needed

## Troubleshooting

### Kibana Won't Start

- Check that Elasticsearch is healthy: `docker compose ps elasticsearch`
- Verify the service token is set: `echo $KIBANA_SERVICE_TOKEN`
- Check Kibana logs: `docker compose logs kibana`

### Authentication Errors

- Verify credentials: `curl -u elastic:password http://localhost:9200`
- Check service status: `docker compose ps`

### Filebeat Connection Issues

- Filebeat is configured with authentication
- Check logs: `docker compose logs filebeat`
