#!/usr/bin/env python3
"""
AI Terminal Client - Universal lightweight client for querying Ollama / Colab Tunnel.
Works out of the box on Kali Linux, Arch Linux, and Windows without external dependencies.
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error

DEFAULT_MODEL = "huihui_ai/qwen2.5-coder-abliterated:14b"
DEFAULT_URL = os.environ.get("LLM_API_URL", "http://localhost:11434")


def query_ollama(base_url, model, prompt, stream=True):
    # Ensure correct base URL without trailing slash
    base_url = base_url.rstrip("/")
    api_endpoint = f"{base_url}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        api_endpoint,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            if stream:
                full_reply = []
                for line in response:
                    line_str = line.decode("utf-8").strip()
                    if not line_str:
                        continue
                    try:
                        chunk = json.loads(line_str)
                        token = chunk.get("response", "")
                        print(token, end="", flush=True)
                        full_reply.append(token)
                    except json.JSONDecodeError:
                        continue
                print()  # newline at end
                return "".join(full_reply)
            else:
                body = response.read().decode("utf-8")
                res_obj = json.loads(body)
                reply = res_obj.get("response", "")
                print(reply)
                return reply
                
    except urllib.error.HTTPError as e:
        print(f"\n[!] HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        try:
            error_body = e.read().decode("utf-8")
            print(f"[!] Detail: {error_body}", file=sys.stderr)
        except Exception:
            pass
        return None
    except urllib.error.URLError as e:
        print(f"\n[!] Connection Error: {e.reason}", file=sys.stderr)
        print("[*] Please verify your Colab Tunnel URL or check if the session is still active.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"\n[!] Unexpected Error: {str(e)}", file=sys.stderr)
        return None


def interactive_mode(base_url, model):
    print("=" * 60)
    print(" Security AI Lab Interactive Terminal")
    print(f" Target URL : {base_url}")
    print(f" Model      : {model}")
    print(" Type 'exit' or 'quit' to leave.")
    print("=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("\n[You] > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("[*] Exiting session.")
                break
            
            print(f"\n[{model}] :")
            query_ollama(base_url, model, user_input, stream=True)
            
        except (KeyboardInterrupt, EOFError):
            print("\n[*] Session terminated.")
            break


def main():
    parser = argparse.ArgumentParser(description="Query Uncensored LLM on Colab/Local for Lab Testing")
    parser.add_argument("prompt", nargs="?", default="", help="Prompt to send to the model")
    parser.add_argument("-u", "--url", default=DEFAULT_URL, help=f"Base URL of Ollama or Tunnel (default: {DEFAULT_URL})")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("-f", "--file", help="Path to code/file to attach with the prompt")
    parser.add_argument("-i", "--interactive", action="store_true", help="Start interactive chat mode")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming response")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode(args.url, args.model)
        return

    full_prompt = args.prompt
    if args.file:
        if not os.path.isfile(args.file):
            print(f"[!] File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            file_content = f.read()
        full_prompt = f"{args.prompt}\n\n```\n# File: {args.file}\n{file_content}\n```"

    if not full_prompt.strip():
        parser.print_help()
        sys.exit(0)

    query_ollama(args.url, args.model, full_prompt, stream=not args.no_stream)


if __name__ == "__main__":
    main()
