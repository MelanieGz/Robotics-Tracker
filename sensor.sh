#!/bin/bash

cleanup() {
  sudo systemctl stop postgresql
  echo "Completed."
  exit 0
}

trap cleanup SIGINT

sudo systemctl start postgresql
uvicorn main:app --host 0.0.0.0 --port 8000 &
python distance.py
