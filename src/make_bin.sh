#!/bin/sh
# This script is used to create the stand-alone
# binary file. To run this script you should 
# install pyinstaller  by using:

# pip install pyinstaller

rm -rf build dist/*

# Create app file using pyinstaller
pyinstaller -F  --name 'Huanbu' \
	        --icon 'huanbu.ico' \
		--windowed  \
		--add-data='strong_beat.wav:.' \
		--add-data='sub_strong_beat.wav:.' \
		--add-data='weak_beat.wav:.' \
		huanbu.py
