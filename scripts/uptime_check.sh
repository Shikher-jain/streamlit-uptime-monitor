#!/bin/bash

echo "Starting uptime check..."
echo "=============================="

apps=$(jq -c '.apps[]' config/apps.json)

pids=()

check_app() {
  app=$1

  name=$(echo $app | jq -r '.name')
  url=$(echo $app | jq -r '.url')
  health=$(echo $app | jq -r '.health')

  echo "-----------------------------"
  echo "Checking: $name"

  health_url="${url%/}${health}"

  success=false

  for i in {1..3}; do
    status=$(curl -L --max-time 10 -o /dev/null -s -w "%{http_code}" "$health_url")

    # fallback to main URL
    if [[ "$status" != "200" ]]; then
      status=$(curl -L --max-time 10 -o /dev/null -s -w "%{http_code}" "$url")
    fi

    if [[ "$status" == "200" || "$status" == "302" || "$status" == "303" ]]; then
      echo "SUCCESS: $name ($status)"
      success=true
      break
    else
      echo "Attempt $i failed for $name ($status)"
      sleep 5
    fi
  done

  if [ "$success" = false ]; then
    echo "FINAL FAILURE: $name"
    return 1
  fi

  return 0
}

# Run all checks in parallel
for app in $apps; do
  check_app "$app" &
  pids+=($!)
done

fail=0

# Wait for all processes
for pid in "${pids[@]}"; do
  wait $pid || fail=1
done

echo "=============================="

if [ $fail -eq 1 ]; then
  echo "❌ Some apps are DOWN"
  exit 1
else
  echo "✅ All apps are UP"
fi
