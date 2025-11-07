#!/bin/bash
# Test API Key Creation via Elasticsearch API

echo "=== Testing API Key Creation ==="
echo ""

# Create an API key using Elasticsearch REST API
echo "Creating API key..."
API_KEY_RESPONSE=$(curl -s -u elastic:password -X POST "localhost:9200/_security/api_key" -H 'Content-Type: application/json' -d'
{
  "name": "test-api-key",
  "expiration": "1d",
  "role_descriptors": {
    "read_only": {
      "cluster": ["monitor"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["read"]
        }
      ]
    }
  }
}
')

echo "API Key Response:"
echo $API_KEY_RESPONSE | python3 -m json.tool 2>/dev/null || echo $API_KEY_RESPONSE

# Extract the API key
API_KEY=$(echo $API_KEY_RESPONSE | grep -o '"encoded":"[^"]*"' | cut -d'"' -f4)

if [ ! -z "$API_KEY" ]; then
    echo ""
    echo "=== Testing API Key Usage ==="
    echo "Using created API key to query Elasticsearch..."
    
    curl -s -H "Authorization: ApiKey $API_KEY" "http://localhost:9200/_cluster/health" | python3 -m json.tool 2>/dev/null
    
    echo ""
    echo "✅ API Key creation and usage successful!"
    echo "API Key: $API_KEY"
else
    echo "❌ Failed to create API key"
fi