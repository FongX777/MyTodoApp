#!/bin/bash
# Complete test script for n8n webhook integration

echo "🎯 MyTodoApp Alert → n8n Webhook Integration Test"
echo "================================================="

function check_services() {
    echo "🔍 Checking service status..."
    echo "   📊 Prometheus: $(curl -s http://localhost:9090/-/healthy && echo "✅ Healthy" || echo "❌ Not responding")"
    echo "   🔔 Alertmanager: $(curl -s http://localhost:9093/-/healthy && echo "✅ Healthy" || echo "❌ Not responding")"
    echo "   🤖 n8n: $(curl -s http://localhost:5678 > /dev/null && echo "✅ Healthy" || echo "❌ Not responding")"
    echo "   🚀 Backend API: $(curl -s http://localhost:8000/healthz > /dev/null && echo "✅ Healthy" || echo "❌ Not responding")"
}

function check_alertmanager_config() {
    echo ""
    echo "🔧 Verifying Alertmanager configuration..."
    CONFIG_CHECK=$(curl -s http://localhost:9093/api/v1/status | python3 -c "
import json
import sys
try:
    data = json.load(sys.stdin)
    config = data.get('data', {}).get('configYAML', '')
    if 'n8n' in config and 'webhook' in config:
        print('✅ n8n webhook configured')
    else:
        print('❌ n8n webhook not found')
except:
    print('❌ Config check failed')
")
    echo "   $CONFIG_CHECK"
}

function trigger_test_alerts() {
    echo ""
    echo "🧪 Generating test errors to trigger alerts..."
    echo "   Sending 40 requests to non-existent endpoints..."
    
    for i in {1..40}; do
        curl -s http://localhost:8000/trigger-404-error > /dev/null 2>&1
        if [ $((i % 10)) -eq 0 ]; then
            echo "   📊 Sent $i requests..."
        fi
    done
    
    echo "   ✅ Error generation completed"
}

function check_prometheus_alerts() {
    echo ""
    echo "📊 Checking Prometheus alert status..."
    ALERTS=$(curl -s http://localhost:9090/api/v1/alerts | python3 -c "
import json
import sys
try:
    data = json.load(sys.stdin)
    alerts = data.get('data', {}).get('alerts', [])
    if alerts:
        for alert in alerts:
            labels = alert.get('labels', {})
            state = alert.get('state', 'unknown')
            print(f'   🔔 {labels.get(\"alertname\", \"Unknown\")} - {state}')
    else:
        print('   ℹ️  No alerts yet (need to wait for evaluation period)')
except:
    print('   ❌ Failed to check alerts')
")
    echo "$ALERTS"
}

function check_alertmanager_alerts() {
    echo ""
    echo "🔔 Checking Alertmanager alert status..."
    AM_ALERTS=$(curl -s http://localhost:9093/api/v1/alerts | python3 -c "
import json
import sys
try:
    data = json.load(sys.stdin)
    alerts = data.get('data', [])
    if alerts:
        for alert in alerts:
            labels = alert.get('labels', {})
            status = alert.get('status', {})
            print(f'   📨 {labels.get(\"alertname\", \"Unknown\")} - {status.get(\"state\", \"unknown\")}')
    else:
        print('   ℹ️  No alerts in Alertmanager yet')
except:
    print('   ❌ Failed to check Alertmanager')
")
    echo "$AM_ALERTS"
}

function show_monitoring_urls() {
    echo ""
    echo "🌐 Monitoring URLs:"
    echo "   📊 Prometheus Alerts: http://localhost:9090/alerts"
    echo "   🔔 Alertmanager: http://localhost:9093"
    echo "   🤖 n8n: http://localhost:5678"
    echo ""
    echo "⏰ Alert Timing:"
    echo "   • Alerts evaluate every 15 seconds"
    echo "   • Must be 'firing' for 5 minutes before sent to Alertmanager"
    echo "   • Alertmanager groups alerts and sends to n8n webhook"
    echo ""
    echo "🔍 To monitor n8n webhook:"
    echo "   1. Open n8n at http://localhost:5678"
    echo "   2. Check your webhook workflow execution history"
    echo "   3. Look for incoming webhook calls from Alertmanager"
}

function wait_for_alerts() {
    echo ""
    echo "⏰ Waiting for alerts to fire (this takes about 5-6 minutes)..."
    echo "   Checking every 30 seconds..."
    
    for i in {1..12}; do
        sleep 30
        echo "   🔄 Check $i/12 ($(($i * 30)) seconds elapsed)"
        
        # Check if we have firing alerts
        FIRING_ALERTS=$(curl -s http://localhost:9090/api/v1/alerts | python3 -c "
import json
import sys
try:
    data = json.load(sys.stdin)
    alerts = data.get('data', {}).get('alerts', [])
    firing = [a for a in alerts if a.get('state') == 'firing']
    print(len(firing))
except:
    print('0')
")
        
        if [ "$FIRING_ALERTS" -gt 0 ]; then
            echo "   🔥 $FIRING_ALERTS alert(s) are now firing!"
            check_alertmanager_alerts
            break
        fi
    done
}

# Main execution
check_services
check_alertmanager_config
trigger_test_alerts
check_prometheus_alerts
show_monitoring_urls

echo ""
echo "🎯 Next Steps:"
echo "   1. Wait 5-6 minutes for alerts to fire"
echo "   2. Check n8n workflow for webhook executions"
echo "   3. Run this script again to see firing alerts: $0"
echo ""
echo "🔄 To wait and monitor automatically:"
echo "   $0 --wait"

if [ "$1" = "--wait" ]; then
    wait_for_alerts
fi