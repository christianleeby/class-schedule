#!/bin/bash
# Hourly: refresh live seats from the ThriveCart checkout → push schedule.json if it changed.
cd "$(dirname "$0")" || exit 1
git pull -q origin main 2>/dev/null
/usr/bin/python3 build.py >/dev/null || exit 1
if ! git diff --quiet -- schedule.json; then
  git add schedule.json && git commit -qm "auto: seats $(date '+%F %H:%M')" && git push -q origin main
  echo "$(date '+%F %H:%M') updated"
fi
