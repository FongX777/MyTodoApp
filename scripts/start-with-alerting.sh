#!/bin/bash
# Script to start all services with alerting and webhook receiver

echo "🚀 Starting MyTodoApp with Alerting & Webhook..."

# Set the Kibana service token
export KIBANA_SERVICE_TOKEN="AAEAAWVsYXN0aWMva2liYW5hL215dG9kb2FwcC1raWJhbmEtdG9rZW4tbmV3OlpnSVdYUElCU0NXWS0zVkg2cUgtQ3c"

echo "1️⃣ Starting webhook receiver in background..."
python3 webhook_receiver.py &
WEBHOOK_PID=$!
echo "   Webhook receiver started with PID: $WEBHOOK_PID"

# Give webhook time to start
sleep 3

echo "2️⃣ Starting all Docker services..."
make dev

echo "3️⃣ Waiting for services to be ready..."
sleep 30

echo "4️⃣ Testing services..."
echo "   📊 Prometheus: http://localhost:9090"
echo "   🔔 Alertmanager: http://localhost:9093" 
echo "   🌐 Webhook receiver: http://localhost:8080"

echo ""
echo "Testing Prometheus connection..."
curl -s http://localhost:9090/-/healthy > /dev/null && echo "   ✅ Prometheus is healthy" || echo "   ❌ Prometheus is not responding"

echo "Testing Alertmanager connection..."
curl -s http://localhost:9093/-/healthy > /dev/null && echo "   ✅ Alertmanager is healthy" || echo "   ❌ Alertmanager is not responding"

echo "Testing webhook receiver..."
curl -s http://localhost:8080 > /dev/null && echo "   ✅ Webhook receiver is healthy" || echo "   ❌ Webhook receiver is not responding"

echo ""
echo "🎯 All services are running!"
echo ""
echo "📍 Access URLs:"
echo "   - Frontend:      http://localhost:3001"
echo "   - Backend API:   http://localhost:8000"
echo "   - API Docs:      http://localhost:8000/docs"
echo "   - Prometheus:    http://localhost:9090"
echo "   - Alertmanager:  http://localhost:9093"
echo "   - Grafana:       http://localhost:3000 (admin/admin)"
echo "   - Kibana:        http://localhost:5601 (elastic/password)"
echo "   - Webhook:       http://localhost:8080"
echo ""
echo "🔥 To trigger test alerts:"
echo "   ./test_alert.sh"
echo ""
echo "🛑 To stop all services:"
echo "   docker compose down && kill $WEBHOOK_PID"
echo ""
echo "💡 Check webhook logs in this terminal..."

# Keep the script running so webhook logs are visible
wait $WEBHOOK_PID