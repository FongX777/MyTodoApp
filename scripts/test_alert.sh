#!/bin/bash
# Test script to trigger alerts by generating errors

echo "Testing alert system by generating HTTP errors..."

# Generate 500 errors to trigger P1_API_01_Critical_Error_Rate (>10% error rate)
for i in {1..20}; do
    curl -s http://localhost:8000/non-existent-endpoint || true
done

echo "Generated 20 requests to non-existent endpoint"
echo "Check Prometheus alerts in 2-3 minutes at: http://localhost:9090/alerts"
echo "Check Grafana dashboards at: http://localhost:3000"