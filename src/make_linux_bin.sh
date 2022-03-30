#!/bin/sh
rm -r build dist/*

# Create app file using pyinstaller
pyinstaller -F  --name 'Huanbu' --icon 'huanbu.ico' --windowed  --add-data='metronome.wav:.' --add-data='metronomeup.wav:.' --add-data='metronomeup_2.wav:.' huanbu.py
