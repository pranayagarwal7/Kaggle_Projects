#!/usr/bin/env bash
# Downloads competition data from Kaggle into data/
# Requires: kaggle CLI configured with ~/.kaggle/kaggle.json
# Setup: pip install kaggle && place your kaggle.json in ~/.kaggle/

set -e

COMPETITION="playground-series-s6e4"
DATA_DIR="$(dirname "$0")/data"

mkdir -p "$DATA_DIR"
kaggle competitions download -c "$COMPETITION" -p "$DATA_DIR"
unzip -o "$DATA_DIR/$COMPETITION.zip" -d "$DATA_DIR"
rm "$DATA_DIR/$COMPETITION.zip"

echo "Data ready in $DATA_DIR"
