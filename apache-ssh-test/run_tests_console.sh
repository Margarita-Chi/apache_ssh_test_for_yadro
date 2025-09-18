#!/usr/bin/env bash
set -euo pipefail

# Directories for logs and Allure 
LOG_DIR="./logs"
ALLURE_RESULTS="./allure-results"
ALLURE_REPORT="./allure-report"

mkdir -p "$LOG_DIR" "$ALLURE_RESULTS" "$ALLURE_REPORT"
chmod 777 "$LOG_DIR" "$ALLURE_RESULTS" "$ALLURE_REPORT"

LOG_FILE="$LOG_DIR/run.log"
COMPOSE="docker compose"
AGENT="agent"
TARGET="target"

echo "=== Running tests (console mode) ===" | tee -a "$LOG_FILE"

# Start target container if not running 
if ! $COMPOSE ps -q $TARGET >/dev/null 2>&1; then
    echo "Target container not found, starting it..." | tee -a "$LOG_FILE"
    $COMPOSE up -d $TARGET >>"$LOG_FILE" 2>&1
else
    echo "Target container is already running." | tee -a "$LOG_FILE"
fi

# Run pytest in agent container
echo "=== Running pytest in agent ===" | tee -a "$LOG_FILE"

$COMPOSE run --rm $AGENT bash -c "
pytest tests/ --alluredir=$ALLURE_RESULTS -v --cache-clear --disable-warnings
" | tee -a "$LOG_FILE"

echo "=== Tests completed ===" | tee -a "$LOG_FILE"
echo "Allure results are located at: $ALLURE_RESULTS" | tee -a "$LOG_FILE"
echo "Log saved at: $LOG_FILE" | tee -a "$LOG_FILE"

