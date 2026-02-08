import requests
import json

# Test the backend API
BASE_URL = "http://localhost:8000"

# Register a new user
def register_user():
    register_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print(f"Register Response Status: {response.status_code}")
    print(f"Register Response: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Registration failed: {response.text}")
        return None

# Login with the registered user
def login_user():
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Login Response Status: {response.status_code}")
    print(f"Login Response: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Login failed: {response.text}")
        return None

if __name__ == "__main__":
    print("Testing registration...")
    register_response = register_user()
    
    print("\nTesting login...")
    login_response = login_user()
    
    if login_response and 'access_token' in login_response:
        print(f"\nSuccess! Got token: {login_response['access_token'][:20]}...")
        
        # Test getting user profile
        headers = {"Authorization": f"Bearer {login_response['access_token']}"}
        profile_response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"\nProfile Response Status: {profile_response.status_code}")
        print(f"Profile Response: {profile_response.text}")