#!/bin/sh
rm -r build dist/*

# Create app file using pyinstaller
pyinstaller -F  --name 'Huanbu' --icon 'huanbu.ico' --windowed  --add-data='strong_beat.wav:.' --add-data='sub_strong_beat.wav:.' --add-data='weak_beat.wav:.' huanbu.py
