#!/bin/bash

echo "📦 Packaging auth_lambda..."

# Clean previous build
rm -rf build_auth
mkdir -p build_auth

# Install dependencies using Lambda-compatible Docker image (python3.8)
docker run --rm -v "$PWD":/var/task -w /var/task lambci/lambda:build-python3.8 \
  pip install -r auth_lambda/requirements.txt -t build_auth/

# Copy app code
cp auth_lambda/main.py build_auth/
cp -r auth_lambda/routes build_auth/
cp models.py build_auth/
# ✅ Add these two:
cp models.py build_auth/
cp -r services build_auth/

# Validate pydantic_core is present
if ! ls build_auth/pydantic_core/_pydantic_core*.so >/dev/null 2>&1; then
  echo "❌ pydantic_core not found — build failed."
  exit 1
fi

# Zip it
cd build_auth
zip -r ../auth_lambda.zip .
cd ..

# Clean up build dir
rm -rf build_auth

echo "✅ Done: auth_lambda.zip created successfully!"
