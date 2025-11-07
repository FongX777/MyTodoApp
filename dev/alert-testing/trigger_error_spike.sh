#!/bin/bash
# Script to trigger error spike for testing Prometheus alerting rules

# Configuration
API_URL=${API_URL:-"http://localhost:8000"}
REQUESTS=${REQUESTS:-200}
ERROR_RATE=${ERROR_RATE:-0.2}  # 20% error rate
PROMETHEUS_URL=${PROMETHEUS_URL:-"http://localhost:9090"}

# Calculate number of errors to generate
ERRORS_TO_GENERATE=$(echo "$REQUESTS * $ERROR_RATE" | bc | cut -d '.' -f 1)

echo "===== Error Spike Generator ====="
echo "API URL: $API_URL"
echo "Total requests: $REQUESTS"
echo "Error rate: $ERROR_RATE"
echo "Error requests to generate: $ERRORS_TO_GENERATE"
echo "==============================="

# Function to generate successful requests
generate_success_requests() {
    local count=$1
    local endpoint="/todos"
    
    echo "Generating $count successful requests..."
    for ((i=1; i<=count; i++)); do
        curl -s -o /dev/null -w "." "$API_URL$endpoint"
        if [ $((i % 50)) -eq 0 ]; then
            echo " $i"
        fi
    done
    echo ""
}

# Function to generate error requests (sending invalid data to trigger 500 errors)
generate_error_requests() {
    local count=$1
    local endpoint="/todos"
    
    echo "Generating $count error requests..."
    for ((i=1; i<=count; i++)); do
        # Send malformed JSON to trigger server error
        curl -s -o /dev/null -w "." -X POST -H "Content-Type: application/json" \
             -d '{"malformed":true, "title": 123, "not_valid": {' \
             "$API_URL$endpoint"
        if [ $((i % 50)) -eq 0 ]; then
            echo " $i"
        fi
    done
    echo ""
}

# Generate a mix of successful and error requests
SUCCESS_REQUESTS=$((REQUESTS - ERRORS_TO_GENERATE))

echo "Starting test at $(date)"
generate_success_requests $SUCCESS_REQUESTS
generate_error_requests $ERRORS_TO_GENERATE
echo "Test completed at $(date)"

# Wait a moment for metrics to update
echo "Waiting for metrics to update..."
sleep 5

# Check if alert is firing in Prometheus
check_alert() {
    echo "Checking if HighErrorRate alert is firing..."
    alert_status=$(curl -s "$PROMETHEUS_URL/api/v1/alerts" | grep -o '"name":"HighErrorRate"')
    
    if [ -n "$alert_status" ]; then
        echo "✅ Alert 'HighErrorRate' is firing!"
    else
        echo "❌ Alert 'HighErrorRate' is not firing. It may take a few minutes for the alert to trigger."
        echo "   Check Prometheus UI at $PROMETHEUS_URL/alerts to monitor status."
    fi
}

check_alert

echo ""
echo "To verify alerts in Prometheus UI:"
echo "1. Open $PROMETHEUS_URL/alerts"
echo "2. Look for 'HighErrorRate' alert in the list"
echo ""
echo "Note: It may take up to 5 minutes for the alert to trigger based on the 'for: 5m' condition."