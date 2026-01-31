#!/bin/bash

DEST="/Volumes/CIRCUITPY"

echo "Stripping typehints, filtering imports, and moving to MC..."

# 1. Backup existing main
cp "$DEST/main.py" "$DEST/last_version.main.py"

# Function to process and move files
process_file() {
    local src=$1
    local target=$2

    # Strip hints to a temp file
    strip-hints "$src" --outfile temp.py

    # Remove lines starting with "from typing import"
    # and save the result to the destination
    sed '/^from typing import/d' temp.py > temp_stripped.py
    ls "$target"
    cp temp_stripped.py "$target"

    # Clean up temp file
    rm temp.py
    rm temp_stripped.py
}

# Process main.py
process_file "main.py" "$DEST/main.py"

# Process cube.py
# Ensure the lib directory exists on the destination first
#mkdir -p "$DEST/lib"
process_file "lib/cube.py" "$DEST/lib/cube.py"

echo "Deploy complete!"