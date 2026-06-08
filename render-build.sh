#!/usr/bin/env bash
# Exit on error
set -o errexit

# Update and install system packages
apt-get update
apt-get install -y ffmpeg

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt
