#!/usr/bin/env bash
set -o errexit

# Determine Hugo version from environment or default to 0.145.0 Extended
HUGO_VER="${HUGO_VERSION:-0.160.1}"

# If hugo is not installed or not the extended edition, download the official extended binary
if ! command -v hugo &> /dev/null || ! hugo version | grep -q "extended"; then
  echo "Installing Hugo v${HUGO_VER} Extended for Linux (amd64)..."
  HUGO_FILE="hugo_extended_${HUGO_VER}_linux-amd64.tar.gz"
  HUGO_URL="https://github.com/gohugoio/hugo/releases/download/v${HUGO_VER}/${HUGO_FILE}"
  
  mkdir -p "$HOME/bin"
  curl -sL "$HUGO_URL" -o "/tmp/$HUGO_FILE"
  tar -xzf "/tmp/$HUGO_FILE" -C "$HOME/bin" hugo
  chmod +x "$HOME/bin/hugo"
  export PATH="$HOME/bin:$PATH"
fi

echo "Verifying Hugo version:"
hugo version

echo "Building site with Hugo..."
hugo --gc --minify

echo "Build complete. Output written to ./public"
