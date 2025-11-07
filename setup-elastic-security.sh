#!/bin/bash
# Script to set up Elasticsearch and Kibana with security enabled

export KIBANA_SERVICE_TOKEN="AAEAAWVsYXN0aWMva2liYW5hL215dG9kb2FwcC1raWJhbmEtdG9rZW4tbmV3OlpnSVdYUElCU0NXWS0zVkg2cUgtQ3c"

echo "Starting services with security enabled..."
docker compose up -d

echo "Waiting for services to start..."
sleep 30

echo "Services status:"
docker compose ps

echo ""
echo "Testing Elasticsearch connection:"
curl -u elastic:password http://localhost:9200/_cat/health

echo ""
echo ""
echo "Access URLs:"
echo "- Elasticsearch: http://localhost:9200 (elastic/changeme)"
echo "- Kibana: http://localhost:5601"
echo "- Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "To create API keys in Kibana:"
echo "1. Go to http://localhost:5601"
echo "2. Navigate to Stack Management > Security > API Keys"
echo "3. Click 'Create API key'"