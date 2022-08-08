#!/bin/bash

echo "Installing addition packages..."
apt get update
apt install ffmpeg
echo "FFMPEG version:"
ffmpeg -version
