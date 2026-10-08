#!/usr/bin/env python3
"""
Colab Setup Script for Ollama + Cloudflare Tunnel
Can be run inside a Google Colab code cell via: !python3 colab_setup.py
"""

import subprocess
import time
import os

MODEL = "huihui_ai/qwen2.5-coder-abliterated:14b"

def run_cmd(cmd, shell=True):
    print(f"[*] Executing: {cmd}")
    res = subprocess.run(cmd, shell=shell, check=True)
    return res

def main():
    print("=== [1/4] Installing Ollama ===")
    run_cmd("curl -fsSL https://ollama.com/install.sh | sh")

    print("\n=== [2/4] Starting Ollama Daemon ===")
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)

    print(f"\n=== [3/4] Pulling Model: {MODEL} ===")
    run_cmd(f"ollama pull {MODEL}")

    print("\n=== [4/4] Setting up Cloudflare Tunnel ===")
    if not os.path.exists("cloudflared-linux-amd64.deb"):
        run_cmd("wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb")
        run_cmd("dpkg -i cloudflared-linux-amd64.deb")

    print("\n" + "=" * 65)
    print(" >>> Look for the URL: https://<random-name>.trycloudflare.com <<<")
    print(" >>> Copy that URL to use in your Kali / Arch / Windows terminal <<<")
    print("=" * 65 + "\n")

    run_cmd("cloudflared tunnel --url http://localhost:11434")

if __name__ == "__main__":
    main()
