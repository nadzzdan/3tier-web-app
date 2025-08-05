import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "3-Tier Web App Backend"}

def test_submit_text_endpoint():
    """Test the submit text endpoint"""
    test_data = {"text": "Test message from CI/CD"}
    response = client.post("/submit", json=test_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

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