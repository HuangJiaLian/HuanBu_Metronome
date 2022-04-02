#!/bin/sh
# This script is used to create the disk 
# image installer on macOS. To run this 
# script you should install pyinstaller
# and create-dmg first by using:

# pip install pyinstaller
# brew install create-dmg

rm -rf build dist/*

#################################################
# Create app file using pyinstaller
#################################################

pyinstaller --name 'Huanbu' \
            --icon 'huanbu.ico' \
            --windowed  \
            --add-data='./strong_beat.wav:.' \
            --add-data='./sub_strong_beat.wav:.' \
            --add-data='./weak_beat.wav:.' \
            huanbu.py


#################################################
# Build the application bundle into a disk image
#################################################

# Create a folder (named dmg) to prepare our DMG in 
# (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -rf dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/Huanbu.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/Huanbu.dmg" && rm "dist/Huanbu.dmg"
create-dmg \
  --volname "Huanbu" \
  --volicon "huanbu.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Huanbu.app" 175 120 \
  --hide-extension "Huanbu.app" \
  --app-drop-link 425 120 \
  "dist/Huanbu.dmg" \
  "dist/dmg/"
