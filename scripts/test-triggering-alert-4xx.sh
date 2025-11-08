#!/bin/bash
# Purpose: Generate sustained 4xx errors to trigger alert thresholds.
# QPS: 10 requests per second for 120 seconds against a non-existent endpoint.
# Report: Summarize counts, latency stats, and error distribution.

set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
DURATION_SECONDS=120
QPS=10
ENDPOINT="/definitely-not-exist"
OUTPUT_DIR="reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="$OUTPUT_DIR/alert_4xx_report_$TIMESTAMP.json"
RAW_LOG="$OUTPUT_DIR/alert_4xx_raw_$TIMESTAMP.log"
mkdir -p "$OUTPUT_DIR"

echo "[INFO] Starting 4xx error generation: $QPS QPS for $DURATION_SECONDS s -> $BASE_URL$ENDPOINT"

# Use background jobs to maintain QPS; each second launch QPS curls.
start_time=$(date +%s)
req_count=0

while true; do
  now=$(date +%s)
  elapsed=$(( now - start_time ))
  if [ $elapsed -ge $DURATION_SECONDS ]; then
    break
  fi
  second_start=$(date +%s%3N)
  for ((i=0;i<QPS;i++)); do
    (
      t0=$(date +%s%3N)
      code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$ENDPOINT") || true
      t1=$(date +%s%3N)
      latency_ms=$(( t1 - t0 ))
      echo "{\"ts\":\"$(date -Iseconds)\",\"code\":$code,\"latency_ms\":$latency_ms}" >> "$RAW_LOG"
    ) &
    req_count=$((req_count+1))
  done
  # Wait remaining of the second
  wait
  sleep 0.05 2>/dev/null || true
done

wait || true

echo "[INFO] Completed sending $req_count requests. Building report..."

# Build report using awk for aggregation (avoid external deps).
report_json=$(awk 'BEGIN{min=1e9;max=0;sum=0;count=0;codes["2xx"]=0;codes["4xx"]=0;codes["5xx"]=0;}{
  if (match($0, /"code":([0-9]{3})/, m) && match($0, /"latency_ms":([0-9]+)/, l)) {
    code=m[1]+0; lat=l[1]+0; count++; sum+=lat; if(lat<min)min=lat; if(lat>max)max=lat;
    if(code>=200 && code<300) codes["2xx"]++;
    else if(code>=400 && code<500) codes["4xx"]++;
    else if(code>=500 && code<600) codes["5xx"]++;
  }
} END{ if(count==0){avg=0;min=0;} else {avg=sum/count;} 
  printf("{\"meta\":{\"qps\":%d,\"duration_seconds\":%d,\"total_requests\":%d},\"latency_ms\":{\"min\":%d,\"max\":%d,\"avg\":%.2f},\"status_groups\":{\"2xx\":%d,\"4xx\":%d,\"5xx\":%d}}", %d, %d, count, min, max, avg, codes["2xx"], codes["4xx"], codes["5xx"]) }' QPS=$QPS DURATION_SECONDS=$DURATION_SECONDS "$RAW_LOG")

echo "$report_json" > "$REPORT_FILE"

cat <<EOF
[INFO] Report saved: $REPORT_FILE
[INFO] Raw log: $RAW_LOG
$(echo "$report_json" | jq . 2>/dev/null || echo "$report_json")
Next steps:
  * Inspect Prometheus/Grafana for alert firing.
  * Correlate with logs in Elasticsearch.
EOF
