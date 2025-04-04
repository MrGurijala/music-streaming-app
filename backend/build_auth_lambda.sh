#!/bin/bash

echo "📦 Packaging auth_lambda..."

# Clean and prepare build folder
rm -rf build_auth
mkdir -p build_auth

# Copy your app code
cp auth_lambda/main.py build_auth/
cp -r auth_lambda/routes build_auth/
cp models.py build_auth/
cp -r services build_auth/

# Install Python dependencies into the build dir
pip install -r auth_lambda/requirements.txt -t build_auth/

# Check pydantic_core exists before zipping
if [[ ! -f build_auth/pydantic_core/_pydantic_core*.so ]]; then
  echo "❌ pydantic_core not found — build failed."
  exit 1
fi

# Zip it
cd build_auth
zip -r ../auth_lambda.zip .
cd ..

# Cleanup
rm -rf build_auth

echo "✅ Done: auth_lambda.zip created!"
