#!/bin/bash
# Double-click this file in Finder, any time after OpenAlex resets.
#
# It picks up where the last run left off — every lookup already done is cached,
# so nothing is fetched twice — and stops on its own when the day's allowance
# runs low, leaving a clean place to start again tomorrow.
#
# OpenAlex gives 1000 credits a day, and looking a work up by its title costs
# 10 of them, so one run covers roughly ninety works. Run it once a day until it
# says nothing is missing. Each run shares its credits out across all the
# studies, so the map fills in evenly rather than one paper at a time.

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

printf '\n  Checking whether OpenAlex has credits left today...\n'
# One lookup by ID costs 1 credit. The title search this used to be cost 10.
hdr=$(curl -s -D - -o /dev/null \
  "https://api.openalex.org/works?filter=openalex_id:W2741809807&per-page=1&select=id&mailto=$OA_MAILTO" 2>/dev/null)
status=$(printf '%s' "$hdr" | awk 'NR==1{gsub(/\r/,""); print $2}')

if [ "$status" = "429" ]; then
  wait_s=$(printf '%s' "$hdr" | awk 'tolower($1)=="retry-after:" {gsub(/\r/,"",$2); print $2}')
  printf '\n  Today'"'"'s credits are already spent.\n'
  printf '  OpenAlex refills them in about %s hours.\n' "$(( (${wait_s:-0} + 1800) / 3600 ))"
  printf '  Nothing was fetched. Run this again after that.\n\n'
  printf '  Press return to close.\n'
  read -r
  exit 0
fi

printf '\n  Resolving cited works against OpenAlex...\n\n'
"$PY" -u resolve_oa.py || { printf '\n  resolve_oa.py stopped. Press return.\n'; read -r; exit 1; }

printf '\n  Working out the second-order structure...\n\n'
"$PY" -u secondorder.py || { printf '\n  secondorder.py stopped. Press return.\n'; read -r; exit 1; }

printf '\n  Done. If it says lookups are still missing, that is the day'"'"'s credits\n'
printf '  running out, not a fault. Run this again tomorrow and it carries on from here.\n\n'
printf '  Press return to close.\n'
read -r
