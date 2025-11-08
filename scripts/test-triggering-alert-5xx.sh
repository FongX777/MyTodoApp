#!/bin/bash
# Purpose: Generate sustained 5xx errors using the /flaky endpoint to trigger alerts.
# QPS: 10 requests per second for 120 seconds against /flaky with wait=300ms errorRate=0.8
# Report: Summarize counts, latency stats, error distribution, observed error rate vs target.

set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
DURATION_SECONDS=120
QPS=10
ENDPOINT="/flaky?wait=300ms&errorRate=0.8"
OUTPUT_DIR="reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="$OUTPUT_DIR/alert_5xx_report_$TIMESTAMP.json"
RAW_LOG="$OUTPUT_DIR/alert_5xx_raw_$TIMESTAMP.log"
mkdir -p "$OUTPUT_DIR"

echo "[INFO] Starting 5xx error generation: $QPS QPS for $DURATION_SECONDS s -> $BASE_URL$ENDPOINT"

start_time=$(date +%s)
req_count=0

while true; do
  now=$(date +%s)
  elapsed=$(( now - start_time ))
  if [ $elapsed -ge $DURATION_SECONDS ]; then
    break
  fi
  for ((i=0;i<QPS;i++)); do
    (
      t0=$(date +%s%3N)
      http_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$ENDPOINT") || true
      t1=$(date +%s%3N)
      latency_ms=$(( t1 - t0 ))
      echo "{\"ts\":\"$(date -Iseconds)\",\"code\":$http_code,\"latency_ms\":$latency_ms}" >> "$RAW_LOG"
    ) &
    req_count=$((req_count+1))
  done
  wait
  sleep 0.05 2>/dev/null || true
done

wait || true

echo "[INFO] Completed sending $req_count requests. Building report..."

report_json=$(awk 'BEGIN{min=1e9;max=0;sum=0;count=0;fail=0;codes["2xx"]=0;codes["4xx"]=0;codes["5xx"]=0;}{
  if (match($0, /"code":([0-9]{3})/, m) && match($0, /"latency_ms":([0-9]+)/, l)) {
    code=m[1]+0; lat=l[1]+0; count++; sum+=lat; if(lat<min)min=lat; if(lat>max)max=lat;
    if(code>=200 && code<300) codes["2xx"]++;
    else if(code>=400 && code<500) codes["4xx"]++;
    else if(code>=500 && code<600) { codes["5xx"]++; fail++; }
  }
} END{ if(count==0){avg=0;min=0;} else {avg=sum/count;} observed=(count?fail/count:0); printf("{\"meta\":{\"qps\":%d,\"duration_seconds\":%d,\"total_requests\":%d,\"target_error_rate\":0.8,\"observed_error_rate\":%.3f},\"latency_ms\":{\"min\":%d,\"max\":%d,\"avg\":%.2f},\"status_groups\":{\"2xx\":%d,\"4xx\":%d,\"5xx\":%d}}", %d, %d, count, observed, min, max, avg, codes["2xx"], codes["4xx"], codes["5xx"]) }' QPS=$QPS DURATION_SECONDS=$DURATION_SECONDS "$RAW_LOG")

echo "$report_json" > "$REPORT_FILE"

cat <<EOF
[INFO] Report saved: $REPORT_FILE
[INFO] Raw log: $RAW_LOG
$(echo "$report_json" | jq . 2>/dev/null || echo "$report_json")
Next steps:
  * Inspect Prometheus/Grafana for 5xx alert firing.
  * Correlate with logs and latency graphs.
EOF
