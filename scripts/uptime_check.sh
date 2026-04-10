#!/bin/bash

echo "🚀 Starting uptime check..."
echo "============================="

apps=$(jq -r '.apps[]' config/apps.json)

for url in $apps; do
  echo "Checking: $url"

  status=$(curl -L --max-time 10 -o /dev/null -s -w "%{http_code}" "$url")

  if [[ "$status" == "200" || "$status" == "301" || "$status" == "302" || "$status" == "303" ]]; then
    echo "✅ UP ($status): $url"
  else
    echo "❌ DOWN ($status): $url"
  fi

  echo "-----------------------------"
done

echo "Done."
