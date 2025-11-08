#!/usr/bin/env bash
# Poll for a new monitor report and copy the first one found to report_for_chat.txt
REPORT_DIR="$(dirname "$0")/monitor_reports"
OUT_FILE="$REPORT_DIR/report_for_chat.txt"
MAX_MINUTES=40
SLEEP_SEC=15
ELAPSED=0

mkdir -p "$REPORT_DIR"
# Wait loop
while [ $ELAPSED -lt $((MAX_MINUTES * 60)) ]; do
  # find the newest report file
  latest=$(ls -1t "$REPORT_DIR"/report_*.txt 2>/dev/null | head -n1)
  if [ -n "$latest" ]; then
    cp "$latest" "$OUT_FILE"
    echo "FOUND and copied $latest to $OUT_FILE"
    exit 0
  fi
  sleep $SLEEP_SEC
  ELAPSED=$((ELAPSED + SLEEP_SEC))
done

echo "TIMEOUT: no report found within ${MAX_MINUTES} minutes" > "$OUT_FILE"
exit 0
