import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct message"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "3-Tier Web App Backend" in data["message"]
    assert "version" in data
    assert data["version"] == "2.0"

def test_submit_text_endpoint():
    """Test the submit text endpoint"""
    test_data = {"text": "Test message from CI/CD v2.0"}
    response = client.post("/submit", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "version" in data
    assert data["version"] == "2.0"

def test_submit_text_empty():
    """Test submit endpoint with empty text"""
    test_data = {"text": ""}
    response = client.post("/submit", json=test_data)
    assert response.status_code == 200  # Should still succeed with empty text

def test_get_texts_endpoint():
    """Test the get texts endpoint"""
    response = client.get("/texts")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 