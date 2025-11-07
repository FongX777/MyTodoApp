#!/bin/bash
# Enhanced test script to trigger different types of alerts and webhook notifications

echo "🧪 Testing Alert System with Webhook Integration..."
echo "======================================================="

function test_error_rate_alert() {
    echo ""
    echo "1️⃣ Testing High Error Rate Alerts (P1_API_01)..."
    echo "   Generating 50 404 errors to trigger >10% error rate..."
    
    # Generate requests to trigger error rate alerts
    for i in {1..50}; do
        curl -s http://localhost:8000/non-existent-endpoint > /dev/null 2>&1 || true
        if [ $((i % 10)) -eq 0 ]; then
            echo "   📊 Generated $i errors..."
        fi
    done
    
    echo "   ✅ Error rate test completed"
}

function test_service_down_alert() {
    echo ""
    echo "2️⃣ Testing Service Down Alert (P1_API_07)..."
    echo "   Note: This would require stopping the backend service"
    echo "   Command: docker compose stop backend"
    echo "   (Not executing automatically to avoid disruption)"
}

function check_alert_status() {
    echo ""
    echo "3️⃣ Checking current alert status..."
    
    echo "   📊 Prometheus Alerts:"
    curl -s http://localhost:9090/api/v1/alerts | python3 -c "
import json
import sys
try:
    data = json.load(sys.stdin)
    alerts = data.get('data', {}).get('alerts', [])
    if alerts:
        for alert in alerts:
            labels = alert.get('labels', {})
            state = alert.get('state', 'unknown')
            print(f'      🔔 {labels.get(\"alertname\", \"Unknown\")} - {state}')
    else:
        print('      ℹ️  No active alerts')
except:
    print('      ❌ Failed to parse alerts')" 2>/dev/null || echo "      ❌ Failed to fetch alerts"

    echo ""
    echo "   🔔 Alertmanager Status:"
    curl -s http://localhost:9093/api/v1/alerts | python3 -c "
import json
import sys
try:
    data = json.load(sys.stdin)
    alerts = data.get('data', [])
    if alerts:
        for alert in alerts:
            labels = alert.get('labels', {})
            status = alert.get('status', {})
            print(f'      📨 {labels.get(\"alertname\", \"Unknown\")} - {status.get(\"state\", \"unknown\")}')
    else:
        print('      ℹ️  No alerts in Alertmanager')
except:
    print('      ❌ Failed to parse Alertmanager alerts')" 2>/dev/null || echo "      ❌ Failed to fetch Alertmanager alerts"
}

function test_webhook_directly() {
    echo ""
    echo "4️⃣ Testing webhook receiver directly..."
    
    # Test webhook with sample alert data
    webhook_test_data='{
        "receiver": "webhook-test",
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {
                    "alertname": "TestAlert",
                    "service": "mytodoapp",
                    "priority": "P1",
                    "severity": "critical",
                    "alert_type": "API",
                    "alert_id": "99"
                },
                "annotations": {
                    "summary": "Test alert for webhook verification",
                    "description": "This is a test alert to verify webhook integration"
                },
                "startsAt": "'$(date -Iseconds)'",
                "endsAt": "0001-01-01T00:00:00Z"
            }
        ],
        "groupLabels": {
            "alertname": "TestAlert"
        },
        "commonLabels": {
            "alertname": "TestAlert",
            "service": "mytodoapp"
        },
        "commonAnnotations": {},
        "externalURL": "http://alertmanager:9093",
        "version": "4",
        "groupKey": "{}:{alertname=\"TestAlert\"}"
    }'
    
    echo "   📡 Sending test alert to webhook..."
    response=$(curl -s -w "%{http_code}" -X POST \
        -H "Content-Type: application/json" \
        -u "webhook_user:webhook_pass" \
        -d "$webhook_test_data" \
        http://localhost:8080/webhook/critical)
    
    http_code="${response: -3}"
    if [ "$http_code" -eq 200 ]; then
        echo "   ✅ Webhook test successful (HTTP $http_code)"
    else
        echo "   ❌ Webhook test failed (HTTP $http_code)"
    fi
}

# Main execution
echo "🎯 Target services:"
echo "   - Backend API: http://localhost:8000"
echo "   - Prometheus: http://localhost:9090"
echo "   - Alertmanager: http://localhost:9093"
echo "   - Webhook: http://localhost:8080"

# Run tests
test_webhook_directly
test_error_rate_alert
check_alert_status

echo ""
echo "📈 Monitor alerts:"
echo "   - Prometheus Alerts: http://localhost:9090/alerts"
echo "   - Alertmanager: http://localhost:9093"
echo "   - Webhook logs: Check the terminal running webhook_receiver.py"
echo ""
echo "⏰ Wait 2-5 minutes for alerts to trigger..."
echo "   Alert rules have a 5-minute evaluation period"
echo ""
echo "🔄 To check status again: $0"
echo "🛑 To trigger service down: docker compose stop backend"
echo "✅ To clear alerts: docker compose restart backend"