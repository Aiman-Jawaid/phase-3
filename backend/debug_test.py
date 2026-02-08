import sys
import traceback
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)

print("Testing the register endpoint...")

try:
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123"
        }
    )
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
except Exception as e:
    print(f"Error making request: {e}")
    traceback.print_exc()

print("\nTesting the health endpoint...")
try:
    response = client.get("/health")
    print(f"Health response status: {response.status_code}")
    print(f"Health response body: {response.json()}")
except Exception as e:
    print(f"Error with health check: {e}")
    traceback.print_exc()