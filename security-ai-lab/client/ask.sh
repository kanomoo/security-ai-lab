#!/usr/bin/env bash
#
# Quick Ask Script for Kali Linux and Arch Linux
# Usage: ./ask.sh [-u https://url.trycloudflare.com] "คำถามที่ต้องการถาม"
#

DEFAULT_URL="${LLM_API_URL:-http://localhost:11434}"
DEFAULT_MODEL="${LLM_MODEL:-huihui_ai/qwen2.5-coder-abliterated:14b}"

URL="$DEFAULT_URL"
MODEL="$DEFAULT_MODEL"

while getopts "u:m:h" opt; do
  case $opt in
    u) URL="$OPTARG" ;;
    m) MODEL="$OPTARG" ;;
    h)
      echo "Usage: $0 [-u URL] [-m MODEL] \"prompt text\""
      exit 0
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

shift $((OPTIND -1))
PROMPT="$*"

if [ -z "$PROMPT" ]; then
  echo "Error: Prompt cannot be empty."
  echo "Usage: $0 [-u URL] \"Your question or task\""
  exit 1
fi

URL="${URL%/}"

echo "[-] Querying $MODEL via $URL..."

curl -s -N -X POST "$URL/api/generate" \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"$MODEL\", \"prompt\": \"$PROMPT\", \"stream\": true}" | while read -r line; do
    token=$(echo "$line" | grep -o '"response":"[^"]*' | sed 's/"response":"//' 2>/dev/null)
    printf "%b" "$token"
done
echo ""
