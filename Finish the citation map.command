#!/bin/bash
# Double-click this file in Finder, any time after OpenAlex resets.
#
# It picks up where the last run left off — every lookup already done is cached,
# so nothing is fetched twice — and stops on its own when the day's allowance
# runs low, leaving a clean place to start again tomorrow.
#
# OpenAlex allows 1000 requests a day per address. Finishing needs about 640 of
# them for the works plus roughly 120 for the ancestors' titles, so one full
# day's allowance is enough with room to spare.

cd "$(dirname "$0")/_generators" || exit 1

PY=/usr/bin/python3          # the system Python; the Homebrew one cannot parse XML

# The contact address OpenAlex asks callers to identify themselves with. It
# lives in a file that git ignores, so it never reaches the public repository.
if [ -f .oa_mailto ]; then
  OA_MAILTO=$(tr -d '[:space:]' < .oa_mailto)
else
  printf '  An email address for OpenAlex to identify you by: '
  read -r OA_MAILTO
fi
export OA_MAILTO

printf '\n  Checking whether OpenAlex has budget today...\n'
status=$(curl -s -o /dev/null -w '%{http_code}' \
  "https://api.openalex.org/works?filter=title.search:test&per-page=1&select=id&mailto=$OA_MAILTO" 2>/dev/null)

if [ "$status" = "429" ]; then
  wait_s=$(curl -s -D - -o /dev/null \
    "https://api.openalex.org/works?filter=title.search:test&per-page=1&select=id&mailto=$OA_MAILTO" \
    2>/dev/null | awk 'BEGIN{IGNORECASE=1} /^retry-after:/ {gsub(/\r/,"",$2); print $2}')
  printf '\n  Today'"'"'s allowance is already spent.\n'
  printf '  It resets at midnight UTC — about %s hours from now.\n' "$((${wait_s:-0} / 3600))"
  printf '  Nothing was fetched. Run this again after that.\n\n'
  printf '  Press return to close.\n'
  read -r
  exit 0
fi

printf '\n  Resolving cited works against OpenAlex...\n\n'
"$PY" -u resolve_oa.py || { printf '\n  resolve_oa.py stopped. Press return.\n'; read -r; exit 1; }

printf '\n  Working out the second-order structure...\n\n'
"$PY" -u secondorder.py || { printf '\n  secondorder.py stopped. Press return.\n'; read -r; exit 1; }

printf '\n  Done. If it says lookups are still missing, the day'"'"'s allowance ran\n'
printf '  out — run this again tomorrow and it will carry on from here.\n\n'
printf '  Press return to close.\n'
read -r
