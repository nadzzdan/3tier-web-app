# Docker Hub + GitHub Actions CI/CD Setup Guide

This guide explains how to set up Docker Hub integration with GitHub Actions for your 3-tier web application.

## Prerequisites

1. **Docker Hub Account**: Create an account at [hub.docker.com](https://hub.docker.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Docker Hub Access Token**: You'll need to create an access token for authentication

## Step-by-Step Setup

### Step 1: Create Docker Hub Access Token

1. Log in to your Docker Hub account
2. Go to **Account Settings** → **Security**
3. Click **New Access Token**
4. Give it a name (e.g., "GitHub Actions CI/CD")
5. Copy the generated token (you won't see it again!)

### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:
   - `DOCKER_HUB_USERNAME`: Your Docker Hub username
   - `DOCKER_HUB_ACCESS_TOKEN`: The access token you created in Step 1

### Step 3: Create Docker Hub Repositories

1. In Docker Hub, create two repositories:
   - `your-username/3tier-backend`
   - `your-username/3tier-frontend`

2. Make sure they are set to **Public** or **Private** as per your preference

### Step 4: Update Docker Compose for Production

Create a production version of your docker-compose.yml that uses the Docker Hub images:

```yaml
version: "3.9"
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    restart: always

  backend:
    image: your-username/3tier-backend:latest
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      - MYSQL_HOST=db
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - APP_HOST=0.0.0.0
      - APP_PORT=8000
      - DEBUG=False
      - ALLOWED_ORIGINS=${ALLOWED_ORIGINS}
    depends_on:
      - db
    restart: always

  frontend:
    image: your-username/3tier-frontend:latest
    ports:
      - "8080:80"
    depends_on:
      - backend
    restart: always

volumes:
  mysql_data:
```

### Step 5: Understanding the CI/CD Pipeline

The workflow file `.github/workflows/docker-hub-ci-cd.yml` includes:

#### **Job 1: Test Backend**
- Runs Python tests before building images
- Ensures code quality before deployment

#### **Job 2: Build and Push**
- Builds Docker images for both backend and frontend
- Pushes to Docker Hub with multiple tags:
  - `latest` for the main branch
  - `{branch-name}-{commit-sha}` for feature branches
  - Semantic version tags for releases

#### **Job 3 & 4: Deployment**
- Optional staging and production deployments
- Can be customized for your deployment strategy

#### **Job 5: Security Scan**
- Scans Docker images for vulnerabilities
- Uploads results to GitHub Security tab

### Step 6: Workflow Triggers

The pipeline triggers on:
- **Push to main/develop branches**: Full CI/CD pipeline
- **Pull requests**: Testing and security scanning only
- **Path changes**: Only runs when relevant files change

### Step 7: Testing the Setup

1. **Make a change** to your backend or frontend code
2. **Commit and push** to the main branch
3. **Check GitHub Actions** tab to see the pipeline running
4. **Verify Docker Hub** to see your images being pushed

### Step 8: Deployment Options

#### Option A: Manual Deployment
```bash
# Pull and run the latest images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

#### Option B: Automated Deployment
Add deployment steps to the workflow:
- **Kubernetes**: Use `kubectl` commands
- **Docker Swarm**: Use `docker stack deploy`
- **Cloud Platforms**: Use platform-specific deployment tools

## Environment Variables

Create a `.env` file for production:

```env
MYSQL_ROOT_PASSWORD=your-secure-password
MYSQL_DATABASE=your-database-name
MYSQL_USER=your-database-user
MYSQL_PASSWORD=your-database-password
APP_PORT=8000
ALLOWED_ORIGINS=https://yourdomain.com
```

## Best Practices

1. **Security**:
   - Never commit secrets to your repository
   - Use GitHub Secrets for sensitive data
   - Regularly rotate Docker Hub access tokens

2. **Image Tagging**:
   - Use semantic versioning for releases
   - Tag with commit SHA for traceability
   - Keep `latest` tag for the most recent stable version

3. **Testing**:
   - Add comprehensive tests to your backend
   - Test Docker images before pushing
   - Use multi-stage builds for smaller images

4. **Monitoring**:
   - Set up alerts for failed builds
   - Monitor Docker Hub rate limits
   - Track deployment success rates

## Troubleshooting

### Common Issues:

1. **Authentication Failed**:
   - Verify Docker Hub credentials in GitHub Secrets
   - Check if the access token has proper permissions

2. **Build Failures**:
   - Check Dockerfile syntax
   - Verify all required files are present
   - Review build logs for specific errors

3. **Push Failures**:
   - Ensure Docker Hub repositories exist
   - Check if you have write permissions
   - Verify image names match repository names

### Useful Commands:

```bash
# Test Docker build locally
docker build -t your-username/3tier-backend:test ./backend

# Test Docker login
docker login -u your-username -p your-access-token

# Check Docker Hub rate limits
curl -H "Authorization: Bearer your-access-token" \
  https://registry-1.docker.io/v2/your-username/3tier-backend/tags/list
```

## Next Steps

1. **Set up monitoring** for your deployed applications
2. **Configure backup strategies** for your database
3. **Implement blue-green deployments** for zero-downtime updates
4. **Add performance testing** to your CI/CD pipeline
5. **Set up automated rollbacks** for failed deployments

This setup provides a robust CI/CD pipeline that automatically builds, tests, and deploys your 3-tier web application using Docker Hub and GitHub Actions. 