#!/bin/sh
rm -r build dist/*

# Create app file using pyinstaller
pyinstaller --name 'Huanbu' --icon 'huanbu.ico' --windowed  --add-data='metronome.wav:.' --add-data='metronomeup.wav:.' --add-data='metronomeup_2.wav:.' huanbu.py

# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
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
