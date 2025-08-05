Write-Host "🧪 Testing Local Docker Setup for CI/CD Pipeline" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Test 1: Check if Docker is running
Write-Host "1. Checking Docker status..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Test 2: Test backend Docker build
Write-Host "2. Testing backend Docker build..." -ForegroundColor Yellow
try {
    docker build -t test-backend ./backend
    Write-Host "✅ Backend Docker build successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend Docker build failed" -ForegroundColor Red
    exit 1
}

# Test 3: Test frontend Docker build
Write-Host "3. Testing frontend Docker build..." -ForegroundColor Yellow
try {
    docker build -t test-frontend ./frontend
    Write-Host "✅ Frontend Docker build successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend Docker build failed" -ForegroundColor Red
    exit 1
}

# Test 4: Test docker-compose
Write-Host "4. Testing docker-compose..." -ForegroundColor Yellow
try {
    docker-compose config | Out-Null
    Write-Host "✅ Docker-compose configuration is valid" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker-compose configuration is invalid" -ForegroundColor Red
    exit 1
}

# Test 5: Test production docker-compose
Write-Host "5. Testing production docker-compose..." -ForegroundColor Yellow
try {
    docker-compose -f docker-compose.prod.yml config | Out-Null
    Write-Host "✅ Production docker-compose configuration is valid" -ForegroundColor Green
} catch {
    Write-Host "❌ Production docker-compose configuration is invalid" -ForegroundColor Red
    exit 1
}

# Clean up test images
Write-Host "6. Cleaning up test images..." -ForegroundColor Yellow
docker rmi test-backend test-frontend 2>$null

Write-Host ""
Write-Host "🎉 All local tests passed! Ready to push to GitHub." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Commit and push your changes to GitHub"
Write-Host "2. Check the GitHub Actions tab to see the pipeline running"
Write-Host "3. Verify images are pushed to Docker Hub"
Write-Host ""
Write-Host "To push your changes:" -ForegroundColor Cyan
Write-Host "git add ."
Write-Host "git commit -m 'Add CI/CD pipeline and tests'"
Write-Host "git push origin main" 