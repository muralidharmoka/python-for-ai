#!/usr/bin/env bash

API_URL="http://127.0.0.1:8000/ask"

QUESTIONS=(
  "Explain Kubernetes in one line"
  "What is a Kubernetes Pod?"
  "Explain ConfigMaps vs Secrets"
)

for q in "${QUESTIONS[@]}"; do
  echo "➡️ Asking: $q"

  curl -v -G "$API_URL" \
    --data-urlencode "q=$q"

  echo ""
  sleep 1
done