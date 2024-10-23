# test_auth_flow.py
import requests
import json

def test_authentication():
    base_url = "http://127.0.0.1:8000"
    
    # 1. Get token
    print("1. Testing token acquisition...")
    token_url = f"{base_url}/auth/token/"
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic J2l0Lm5ldGZhcm0ubXltZWRib29rLndlYic6"
    }
    token_data = {
        "username": "iskender.wolfer@gmail.com",
        "password": "7879Hi@@@"
    }
    
    try:
        # Get token
        token_response = requests.post(token_url, headers=token_headers, data=token_data)
        print(f"Token Response Status: {token_response.status_code}")
        print(f"Token Response: {token_response.text}\n")
        
        if token_response.status_code == 200:
            token_data = token_response.json()
            access_token = token_data.get('access_token')
            
            # Create headers for authenticated requests
            auth_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # 2. Verify token
            print("2. Testing token verification...")
            verify_url = f"{base_url}/auth/verify/"
            verify_response = requests.get(verify_url, headers=auth_headers)
            print(f"Verify Response Status: {verify_response.status_code}")
            print(f"Verify Response: {verify_response.text}\n")
            
            # 3. Test protected profile endpoint
            print("3. Testing protected profile endpoint...")
            profile_url = f"{base_url}/api/profile/"
            profile_response = requests.get(profile_url, headers=auth_headers)
            print(f"Profile Response Status: {profile_response.status_code}")
            print(f"Profile Response: {profile_response.text}\n")
            
            # 4. Test protected resource creation
            print("4. Testing protected resource creation...")
            resource_url = f"{base_url}/api/resource/"
            resource_data = {
                "name": "Test Resource",
                "description": "This is a test resource"
            }
            resource_response = requests.post(
                resource_url,
                headers=auth_headers,
                json=resource_data
            )
            print(f"Resource Response Status: {resource_response.status_code}")
            print(f"Resource Response: {resource_response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Starting authentication flow test...\n")
    test_authentication()