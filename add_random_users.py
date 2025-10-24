"""
Script to add random user records to the database
"""
import requests
import random
from faker import Faker

BASE_URL = "http://127.0.0.1:8000"
fake = Faker('pl_PL')  # Polish locale for realistic Polish names

# List of possible roles
ROLES = ['admin', 'user', 'moderator', 'editor', 'viewer', 'contributor', 'manager', 'developer']

def generate_random_user():
    """Generate a random user with realistic data"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    full_name = f"{first_name} {last_name}"
    
    # Generate email based on name
    email_formats = [
        f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}",
        f"{first_name[0].lower()}{last_name.lower()}@{fake.free_email_domain()}",
        f"{first_name.lower()}{random.randint(1, 999)}@{fake.free_email_domain()}"
    ]
    email = random.choice(email_formats)
    
    role = random.choice(ROLES)
    
    return {
        "name": full_name,
        "email": email,
        "role": role
    }

def add_random_users(count=1):
    """Add specified number of random users to the database"""
    print(f"\n🎲 Generating and adding {count} random user(s)...\n")
    
    added_users = []
    failed_users = []
    
    for i in range(count):
        user_data = generate_random_user()
        
        try:
            response = requests.post(f"{BASE_URL}/users/", json=user_data)
            
            if response.status_code == 200:
                created_user = response.json()
                added_users.append(created_user)
                print(f"✅ User {i+1}/{count} added successfully:")
                print(f"   ID: {created_user['id']}")
                print(f"   Name: {created_user['name']}")
                print(f"   Email: {created_user['email']}")
                print(f"   Role: {created_user['role']}\n")
            else:
                failed_users.append((user_data, response.json()))
                print(f"❌ User {i+1}/{count} failed: {response.json()['detail']}")
                print(f"   Tried: {user_data['email']}\n")
        
        except requests.exceptions.ConnectionError:
            print("\n❌ Error: Cannot connect to API server!")
            print("Make sure the server is running: uvicorn myapi:app --reload")
            return
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            failed_users.append((user_data, str(e)))
    
    # Summary
    print("\n" + "="*60)
    print(f"📊 Summary:")
    print(f"   Successfully added: {len(added_users)}")
    print(f"   Failed: {len(failed_users)}")
    print("="*60 + "\n")
    
    # Show all users
    if added_users:
        print("📋 All users in database:")
        response = requests.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            all_users = response.json()
            print(f"   Total users: {len(all_users)}\n")
            for user in all_users[-10:]:  # Show last 10 users
                print(f"   • {user['name']} ({user['email']}) - {user['role']}")

if __name__ == "__main__":
    # Add 5 random users
    add_random_users(5)
