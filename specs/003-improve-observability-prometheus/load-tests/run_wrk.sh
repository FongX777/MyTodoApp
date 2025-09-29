#!/bin/bash
# Load test script for AlertingScout API

# Configuration
API_URL=${API_URL:-"http://localhost:8000"}
DURATION=${DURATION:-"30s"}
CONNECTIONS=${CONNECTIONS:-10}
THREADS=${THREADS:-2}
TEST_ENDPOINTS=(
  "/todos"
  "/projects"
  "/"
  "/metrics"
)

# Check if wrk is installed
if ! command -v wrk &> /dev/null; then
    echo "wrk not found. Please install wrk first."
    echo "macOS: brew install wrk"
    echo "Linux: apt install wrk or equivalent"
    exit 1
fi

# Create results directory
RESULTS_DIR="./results_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

echo "===== AlertingScout API Load Test ====="
echo "API URL: $API_URL"
echo "Duration: $DURATION"
echo "Connections: $CONNECTIONS"
echo "Threads: $THREADS"
echo "Results will be saved to: $RESULTS_DIR"
echo "======================================="

# Function to run tests for each endpoint
run_test_for_endpoint() {
    local endpoint=$1
    local output_file="$RESULTS_DIR/result_$(echo $endpoint | tr '/' '_').txt"
    
    echo "Testing endpoint: $endpoint"
    echo "Running: wrk -t$THREADS -c$CONNECTIONS -d$DURATION $API_URL$endpoint"
    
    wrk -t$THREADS -c$CONNECTIONS -d$DURATION "$API_URL$endpoint" > "$output_file"
    
    # Extract key metrics
    local requests=$(grep "requests" "$output_file" | awk '{print $1}')
    local rps=$(grep "Requests/sec" "$output_file" | awk '{print $2}')
    local latency=$(grep "Latency" "$output_file" | awk '{print $2}')
    local p90=$(grep "90%" "$output_file" | awk '{print $2}')
    local p99=$(grep "99%" "$output_file" | awk '{print $2}')
    
    echo "  Results:"
    echo "  - Total requests: $requests"
    echo "  - Requests/sec: $rps"
    echo "  - Avg latency: $latency"
    echo "  - p90 latency: $p90"
    echo "  - p99 latency: $p99"
    echo ""
}

# Run tests for each endpoint
for endpoint in "${TEST_ENDPOINTS[@]}"; do
    run_test_for_endpoint "$endpoint"
done

# Summarize results
echo "Load test complete. Results saved to $RESULTS_DIR"
echo "To compare with baseline, run the same test without observability instrumentation enabled"