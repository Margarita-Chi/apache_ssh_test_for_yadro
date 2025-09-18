#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="./logs"
ALLURE_RESULTS="./allure-results"
ALLURE_REPORT="./allure-report"

COMPOSE="docker compose"
AGENT="agent"
TARGET="target"

echo "=== Stopping containers and network ==="

# Stop and remove all containers and orphaned ones
$COMPOSE down --remove-orphans

echo "=== Cleaning temporary session files ==="

# Change ownership to current user
sudo chown -R $USER:$USER "$LOG_DIR" "$ALLURE_RESULTS" "$ALLURE_REPORT" 2>/dev/null || true

# Give full read/write/execute permissions to user
chmod -R u+rwX "$LOG_DIR" "$ALLURE_RESULTS" "$ALLURE_REPORT" 2>/dev/null || true

# Remove temporary directories
rm -rf "$LOG_DIR" "$ALLURE_RESULTS" "$ALLURE_REPORT" 2>/dev/null || true

echo "=== Cleanup completed ==="

