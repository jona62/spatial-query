#!/bin/bash

csv_file="$1"
json_file="McDonalds.json"

echo "Converting CSV: $csv_file file to JSON"

yq "$csv_file" -p=csv -o=json > "$json_file" 

echo "Output JSON: $json_file"