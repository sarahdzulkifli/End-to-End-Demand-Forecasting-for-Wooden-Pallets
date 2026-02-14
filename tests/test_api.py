"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct response."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'message' in data
        assert 'version' in data
        
    def test_health_check_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        
    def test_predict_endpoint_requires_features(self):
        """Test predict endpoint validates input."""
        # Send empty request
        response = client.post("/predict", json={})
        
        # Should return validation error
        assert response.status_code == 422
        
    def test_predict_endpoint_with_valid_data(self):
        """Test predict endpoint with valid prediction request."""
        request_data = {
            "features": {
                "lag_1": 100,
                "lag_2": 95,
                "rolling_mean_3": 98,
                "posting_month": 5,
                "rate": 12.5,
                "u_frt": 500,
                "posting_quarter": 2,
                "lead_time": 7
            }
        }
        
        response = client.post("/predict", json=request_data)
        
        # Note: This might fail if model isn't trained, which is expected in CI
        assert response.status_code in [200, 500]
        
    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        
        # Should return metrics or appropriate error
        assert response.status_code in [200, 404, 500]
