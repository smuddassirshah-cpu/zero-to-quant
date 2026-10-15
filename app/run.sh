#!/usr/bin/env sh
# Serves the app on http://localhost:8080 (content and Pyodide need http, not file://).
cd "$(dirname "$0")" && exec python3 -m http.server "${1:-8080}"
