#!/bin/bash

echo "📦 Packaging songs_lambda..."

# Clean previous build
rm -rf build_songs
mkdir -p build_songs

# Install dependencies using Lambda-compatible Docker image (python3.8)
docker run --rm -v "$PWD":/var/task -w /var/task lambci/lambda:build-python3.8 \
  pip install -r songs_lambda/requirements.txt -t build_songs/

# Copy app code
cp songs_lambda/main.py build_songs/
cp -r songs_lambda/routes build_songs/
cp models.py build_songs/
# ✅ Add these two:
cp models.py build_songs/
cp -r services build_songs/

# Validate pydantic_core is present
if ! ls build_songs/pydantic_core/_pydantic_core*.so >/dev/null 2>&1; then
  echo "❌ pydantic_core not found — build failed."
  exit 1
fi

# Zip it
cd build_songs
zip -r ../songs_lambda.zip .
cd ..

# Clean up build dir
rm -rf build_songs

echo "✅ Done: songs_lambda.zip created successfully!"
