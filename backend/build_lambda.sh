#!/bin/bash

# 1. Build songs_lambda.zip
echo "📦 Packaging songs_lambda..."
mkdir -p build_songs
cp songs_lambda/main.py build_songs/
cp models.py build_songs/
cp -r services build_songs/
pip install -r songs_lambda/requirements.txt -t build_songs/
cd build_songs
zip -r ../songs_lambda.zip .
cd ..
rm -rf build_songs

# 2. Build auth_lambda.zip
echo "📦 Packaging auth_lambda..."
mkdir -p build_auth
cp auth_lambda/main.py build_auth/
cp models.py build_auth/
cp -r services build_auth/
pip install -r auth_lambda/requirements.txt -t build_auth/
cd build_auth
zip -r ../auth_lambda.zip .
cd ..
rm -rf build_auth

echo "✅ Done: songs_lambda.zip and auth_lambda.zip created!"
