#!/bin/bash

echo "Starting load test for AlertingScout API..."
echo "This will generate metrics for Prometheus and logs for the ELK stack."

# 設置默認參數
DURATION=${1:-5}  # 預設運行 5 分鐘
INTERVAL=${2:-0.5}  # 預設 0.5 秒請求間隔
API_URL="http://localhost:8000"  # 預設 API URL

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not found."
    exit 1
fi

# 安裝必要的 Python 套件（如果尚未安裝）
echo "Checking and installing required Python packages..."
pip3 install requests --quiet

# 執行負載測試
echo "Running load test for $DURATION minutes with $INTERVAL second intervals..."
python3 "$(dirname "$0")/load_test.py" $DURATION $INTERVAL --url $API_URL

echo "Load test completed!"
echo ""
echo "You should now be able to see metrics in Prometheus/Grafana and logs in the ELK stack."
echo "Visit these URLs to view the results:"
echo "- Grafana: http://localhost:3000"
echo "- Prometheus: http://localhost:9090"
echo "- Kibana: http://localhost:5601"