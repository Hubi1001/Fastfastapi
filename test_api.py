"""
Test script for FastAPI application
Tests all CRUD operations on the User API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def print_response(response, title):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"📌 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    print("\n🚀 Starting API Tests...\n")
    
    # 1. Test root endpoint
    print("\n1️⃣ Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "GET /")
    
    # 2. Get all users (should be empty initially)
    print("\n2️⃣ Getting all users (initial state)...")
    response = requests.get(f"{BASE_URL}/users/")
    print_response(response, "GET /users/")
    
    # 3. Create first user
    print("\n3️⃣ Creating first user...")
    user1_data = {
        "name": "Jan Kowalski",
        "email": "jan.kowalski@example.com",
        "role": "admin"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user1_data)
    print_response(response, "POST /users/ (Jan Kowalski)")
    user1_id = response.json()["id"] if response.status_code == 200 else None
    
    # 4. Create second user
    print("\n4️⃣ Creating second user...")
    user2_data = {
        "name": "Anna Nowak",
        "email": "anna.nowak@example.com",
        "role": "user"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user2_data)
    print_response(response, "POST /users/ (Anna Nowak)")
    user2_id = response.json()["id"] if response.status_code == 200 else None
    
    # 5. Create third user
    print("\n5️⃣ Creating third user...")
    user3_data = {
        "name": "Piotr Wiśniewski",
        "email": "piotr.wisniewski@example.com",
        "role": "moderator"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user3_data)
    print_response(response, "POST /users/ (Piotr Wiśniewski)")
    user3_id = response.json()["id"] if response.status_code == 200 else None
    
    # 6. Try to create duplicate email (should fail)
    print("\n6️⃣ Trying to create user with duplicate email...")
    response = requests.post(f"{BASE_URL}/users/", json=user1_data)
    print_response(response, "POST /users/ (Duplicate email)")
    
    # 7. Get all users
    print("\n7️⃣ Getting all users...")
    response = requests.get(f"{BASE_URL}/users/")
    print_response(response, "GET /users/")
    
    # 8. Get specific user by ID
    if user1_id:
        print(f"\n8️⃣ Getting user by ID ({user1_id})...")
        response = requests.get(f"{BASE_URL}/users/{user1_id}")
        print_response(response, f"GET /users/{user1_id}")
    
    # 9. Update user (full update)
    if user2_id:
        print(f"\n9️⃣ Updating user {user2_id}...")
        update_data = {
            "name": "Anna Kowalska",
            "email": "anna.kowalska@example.com",
            "role": "admin"
        }
        response = requests.put(f"{BASE_URL}/users/{user2_id}", json=update_data)
        print_response(response, f"PUT /users/{user2_id}")
    
    # 10. Partial update (only name)
    if user3_id:
        print(f"\n🔟 Partial update of user {user3_id} (only role)...")
        update_data = {
            "role": "super_admin"
        }
        response = requests.put(f"{BASE_URL}/users/{user3_id}", json=update_data)
        print_response(response, f"PUT /users/{user3_id} (partial)")
    
    # 11. Get all users after updates
    print("\n1️⃣1️⃣ Getting all users after updates...")
    response = requests.get(f"{BASE_URL}/users/")
    print_response(response, "GET /users/ (after updates)")
    
    # 12. Try to get non-existent user
    print("\n1️⃣2️⃣ Trying to get non-existent user...")
    response = requests.get(f"{BASE_URL}/users/9999")
    print_response(response, "GET /users/9999")
    
    # 13. Delete user
    if user1_id:
        print(f"\n1️⃣3️⃣ Deleting user {user1_id}...")
        response = requests.delete(f"{BASE_URL}/users/{user1_id}")
        print_response(response, f"DELETE /users/{user1_id}")
    
    # 14. Verify deletion
    print("\n1️⃣4️⃣ Getting all users after deletion...")
    response = requests.get(f"{BASE_URL}/users/")
    print_response(response, "GET /users/ (after deletion)")
    
    # 15. Try to delete non-existent user
    print("\n1️⃣5️⃣ Trying to delete non-existent user...")
    response = requests.delete(f"{BASE_URL}/users/9999")
    print_response(response, "DELETE /users/9999")
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server!")
        print("Make sure the server is running: uvicorn myapi:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
