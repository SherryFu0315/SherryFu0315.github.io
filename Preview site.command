#!/bin/bash
# Double-click this file in Finder.
#
# It rebuilds the site from your edits and opens it in a browser. Leave the
# window open while you are looking at the site; close it when you are done.
#
# After editing words.py or projects.py, just run this again.

cd "$(dirname "$0")" || exit 1

PY=/usr/bin/python3          # the system Python; the Homebrew one cannot parse XML
PORT=8731

printf '\n  Rebuilding the site...\n\n'

cd _generators || { echo "  Could not find the _generators folder."; read -r; exit 1; }

fail=0
for script in build.py build_universe.py build_pages.py; do
  if out=$("$PY" "$script" 2>&1); then
    printf '  ok   %-20s %s\n' "$script" "$(echo "$out" | tail -1)"
  else
    printf '\n  PROBLEM in %s\n\n%s\n' "$script" "$out"
    fail=1
    break                       # stop here rather than pile up more errors
  fi
done
cd ..

if [ "$fail" = 1 ]; then
  printf '\n  The site was not fully rebuilt, so some pages still show the old text.\n'
  printf '  The message above says what went wrong — most often a missing quote mark\n'
  printf '  in words.py or projects.py. The line number it gives is where to look.\n'
  printf '  Fix that and run this again, or send the message above to Claude.\n\n'
  printf '  Press return to close.\n'
  read -r
  exit 1
fi

# stop a server left running from last time, then start a fresh one
lsof -ti tcp:$PORT 2>/dev/null | xargs kill 2>/dev/null
"$PY" -m http.server $PORT --directory "$(pwd)" >/dev/null 2>&1 &
SERVER=$!
sleep 1

printf '\n  Rebuilt. Opening http://localhost:%s\n' "$PORT"
open "http://localhost:$PORT/"

printf '\n  The site is running from this window.\n'
printf '  Press Control-C, or close this window, when you are finished.\n\n'

trap 'kill $SERVER 2>/dev/null' EXIT
wait $SERVER
