#!/usr/bin/env bash
set -o errexit

HUGO_VER="${HUGO_VERSION:-0.160.1}"

# Ensure $HOME/bin is prioritized in PATH
mkdir -p "$HOME/bin"
export PATH="$HOME/bin:$PATH"

# Download and install target Hugo Extended version if missing or version mismatch
if ! command -v hugo &> /dev/null || ! hugo version | grep -q "v${HUGO_VER}"; then
  echo "Installing Hugo v${HUGO_VER} Extended for Linux (amd64)..."
  HUGO_FILE="hugo_extended_${HUGO_VER}_linux-amd64.tar.gz"
  HUGO_URL="https://github.com/gohugoio/hugo/releases/download/v${HUGO_VER}/${HUGO_FILE}"
  
  curl -sL "$HUGO_URL" -o "/tmp/$HUGO_FILE"
  tar -xzf "/tmp/$HUGO_FILE" -C "$HOME/bin" hugo
  chmod +x "$HOME/bin/hugo"
fi

echo "Verifying Hugo version:"
hugo version

echo "Building site with Hugo..."
hugo --gc --minify

echo "Build complete. Output written to ./public"
