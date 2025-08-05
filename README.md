# 3-Tier Web Application

A modern 3-tier web application built with FastAPI, MySQL, and Docker. This application allows users to submit and view text entries through a web interface.

## 🏗️ Architecture

This application follows the classic 3-tier architecture:

- **Presentation Tier**: HTML/JavaScript frontend served by Nginx
- **Application Tier**: FastAPI Python backend API
- **Data Tier**: MySQL database for data persistence

## 🚀 Features

- ✅ Text submission and storage
- ✅ Real-time text display
- ✅ Docker containerization
- ✅ Environment variable configuration
- ✅ CORS support
- ✅ Error handling and user feedback
- ✅ Responsive web design

## 📋 Prerequisites

Before running this application, make sure you have:

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- Git (for cloning the repository)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd 3tier-web-app
```

### 2. Environment Configuration

Create a `.env` file in the `backend/` directory:

```bash
# Database Configuration
MYSQL_HOST=db
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_DATABASE=textsdb

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
```

### 3. Build and Run

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access the Application

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
3tier-web-app/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile         # Backend container config
│   └── .env              # Environment variables (not in git)
├── frontend/
│   └── index.html         # Web interface
├── docker-compose.yml     # Multi-container orchestration
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 API Endpoints

### GET `/texts`
Retrieve all stored texts.

**Response:**
```json
[
  {
    "id": 1,
    "text": "Sample text",
    "created_at": "2025-08-05T03:47:15"
  }
]
```

### POST `/submit`
Submit a new text entry.

**Request Body:**
```json
{
  "text": "Your text here"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Text saved successfully"
}
```

## 🔒 Security Features

- Environment variables for sensitive configuration
- CORS protection
- Input validation
- Error handling

## 🐳 Docker Services

- **db**: MySQL 8.0 database
- **backend**: FastAPI application
- **frontend**: Nginx web server

## 🚀 Deployment

### Local Development
```bash
docker-compose up -d
```

### Production
1. Update `.env` file with production values
2. Set `DEBUG=False`
3. Configure proper CORS origins
4. Use production database credentials

## 🛠️ Development

### Adding New Features
1. Modify `backend/app.py` for new API endpoints
2. Update `frontend/index.html` for UI changes
3. Test with `docker-compose restart`

### Database Changes
1. Modify the `init_db()` function in `app.py`
2. Restart the backend service: `docker-compose restart backend`

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Support

If you encounter any issues or have questions:

1. Check the logs: `docker-compose logs`
2. Verify environment variables
3. Ensure all services are running: `docker-compose ps`
4. Create an issue in the repository

## 🔄 Updates

To update the application:

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build
``` 