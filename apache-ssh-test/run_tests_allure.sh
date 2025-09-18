#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="./logs"
ALLURE_RESULTS="./allure-results"
ALLURE_REPORT="./allure-report"

# Create directories with write permissions 
mkdir -p "$LOG_DIR" "$ALLURE_RESULTS" "$ALLURE_REPORT"
chmod 777 "$LOG_DIR" "$ALLURE_RESULTS" "$ALLURE_REPORT"

LOG_FILE="$LOG_DIR/run.log"
COMPOSE="docker compose"
AGENT="agent"
TARGET="target"

echo "=== Running tests and Allure (no console output) ===" | tee -a "$LOG_FILE"

# Start target container if not running 
if ! $COMPOSE ps -q $TARGET >/dev/null 2>&1; then
    echo "Target container not found, starting it..." | tee -a "$LOG_FILE"
    $COMPOSE up -d $TARGET >>"$LOG_FILE" 2>&1
else
    echo "Target container is already running." | tee -a "$LOG_FILE"
fi

# Run pytest and generate Allure report
$COMPOSE run --rm $AGENT bash -c "
pytest tests/ --alluredir=$ALLURE_RESULTS -v --disable-warnings &&
allure generate $ALLURE_RESULTS -o $ALLURE_REPORT --clean
" >>"$LOG_FILE" 2>&1

# 3. Find a free host port
HOST_PORT=$(python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
port = s.getsockname()[1]
s.close()
print(port)
PY
)

echo "=== Starting Allure web server on port $HOST_PORT ===" | tee -a "$LOG_FILE"

# Run Allure web server
$COMPOSE run --rm -p ${HOST_PORT}:8080 $AGENT bash -c "
allure open $ALLURE_REPORT --port 8080
" >>"$LOG_FILE" 2>&1 &

echo "Report available at: http://localhost:${HOST_PORT}/"
echo "All logs saved at: $LOG_FILE"

