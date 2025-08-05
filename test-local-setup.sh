#!/bin/bash

echo "🧪 Testing Local Docker Setup for CI/CD Pipeline"
echo "================================================"

# Test 1: Check if Docker is running
echo "1. Checking Docker status..."
if docker info > /dev/null 2>&1; then
    echo "✅ Docker is running"
else
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Test 2: Test backend Docker build
echo "2. Testing backend Docker build..."
if docker build -t test-backend ./backend; then
    echo "✅ Backend Docker build successful"
else
    echo "❌ Backend Docker build failed"
    exit 1
fi

# Test 3: Test frontend Docker build
echo "3. Testing frontend Docker build..."
if docker build -t test-frontend ./frontend; then
    echo "✅ Frontend Docker build successful"
else
    echo "❌ Frontend Docker build failed"
    exit 1
fi

# Test 4: Test docker-compose
echo "4. Testing docker-compose..."
if docker-compose config > /dev/null 2>&1; then
    echo "✅ Docker-compose configuration is valid"
else
    echo "❌ Docker-compose configuration is invalid"
    exit 1
fi

# Test 5: Test production docker-compose
echo "5. Testing production docker-compose..."
if docker-compose -f docker-compose.prod.yml config > /dev/null 2>&1; then
    echo "✅ Production docker-compose configuration is valid"
else
    echo "❌ Production docker-compose configuration is invalid"
    exit 1
fi

# Clean up test images
echo "6. Cleaning up test images..."
docker rmi test-backend test-frontend 2>/dev/null || true

echo ""
echo "🎉 All local tests passed! Ready to push to GitHub."
echo ""
echo "Next steps:"
echo "1. Commit and push your changes to GitHub"
echo "2. Check the GitHub Actions tab to see the pipeline running"
echo "3. Verify images are pushed to Docker Hub"
echo ""
echo "To push your changes:"
echo "git add ."
echo "git commit -m 'Add CI/CD pipeline and tests'"
echo "git push origin main" 