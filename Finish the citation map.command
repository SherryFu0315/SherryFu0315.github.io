#!/bin/bash
# Double-click this file in Finder once a day, any time after OpenAlex resets.
#
# It picks up where the last run left off (every lookup already done is cached,
# so nothing is fetched twice) and stops on its own when the day's credits run
# low, leaving a clean place to start again tomorrow. Then it rebuilds the
# research map from the new data, shows which works the map names now, and asks
# before putting the update on the website.
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

# ---- rebuild the map, then ask before publishing -----------------------------
cd .. || exit 1
LOG=$(mktemp -t citation-map)
printf '\n  Rebuilding the research map from the new data...\n\n'
if ! ( cd _generators && "$PY" -B build_universe.py ) > "$LOG" 2>&1; then
  cat "$LOG"; rm -f "$LOG"
  printf '\n  The rebuild stopped, so the website was not touched.\n'
  printf '  Send the message above to Claude. Press return to close.\n'
  read -r; exit 1
fi
grep -E '^deep sky|^  (note|hover|held)' "$LOG" | sed 's/^/  /'
printf '\n  Those are the works the map names today. If one looks wrong, tell\n'
printf '  Claude and it will be kept off the map.\n'

# Only the files a run can change are ever published from here.
FILES="_generators/oa_level1.json _generators/secondorder.json _generators/oa_level2_meta.json universe/index.html"
if git diff --quiet -- $FILES; then
  printf '\n  Nothing on the map changed, so there is nothing to publish.\n'
elif ! git diff --quiet -- _generators/*.py; then
  printf '\n  The map is rebuilt, but some of the site'"'"'s own files have edits that\n'
  printf '  are not published yet, so it will not publish from here. Ask Claude.\n'
else
  printf '\n  Put the updated map on the website now? Type y and press return,\n'
  printf '  or just press return to keep it on this computer: '
  read -r answer
  if [ "$answer" = y ] || [ "$answer" = Y ]; then
    traced=$(grep -o 'traced [0-9]*/[0-9]*' "$LOG" | head -1 | cut -d' ' -f2)
    if git commit -q -m "Citation map: OpenAlex run of $(date +%Y-%m-%d), ${traced:-more} references traced" -- $FILES \
       && git push -q origin HEAD; then
      printf '\n  Published. The website shows it within a couple of minutes.\n'
    else
      printf '\n  Publishing did not go through. The map is saved on this computer;\n'
      printf '  ask Claude to push it.\n'
    fi
  else
    printf '\n  Kept on this computer. Ask Claude to publish it whenever you like.\n'
  fi
fi
rm -f "$LOG"

printf '\n  If it said lookups are still missing, that is the day'"'"'s credits running\n'
printf '  out, not a fault. Run this again tomorrow and it carries on from here.\n\n'
printf '  Press return to close.\n'
read -r
