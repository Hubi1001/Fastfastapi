"""
Script to add random user records through the API (the server must be running).
Names are Polish (Faker pl_PL); e-mail addresses are converted to plain ASCII so they pass validation.
"""
import random
import sys
import unicodedata

import requests
from faker import Faker

BASE_URL = "http://127.0.0.1:8000"
fake = Faker("pl_PL")  # Polish locale for realistic Polish names

ROLES = ["admin", "user", "moderator", "editor", "viewer", "contributor", "manager", "developer"]


def to_email_part(text: str) -> str:
    """'Anna Maria Żółć-Łata' -> 'annamariazolclata' (ł has no Unicode decomposition, so it is mapped by hand)."""
    text = text.replace("ł", "l").replace("Ł", "L")
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return "".join(ch for ch in ascii_text.lower() if ch.isalnum())


def generate_random_user():
    """Generate a random user with realistic data"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    first, last = to_email_part(first_name), to_email_part(last_name)
    domain = fake.free_email_domain()
    email = random.choice([
        f"{first}.{last}@{domain}",
        f"{first[0]}{last}@{domain}",
        f"{first}{random.randint(1, 999)}@{domain}",
    ])
    return {"name": f"{first_name} {last_name}", "email": email, "role": random.choice(ROLES)}


def add_random_users(count=1):
    """Add the given number of random users and print a summary."""
    print(f"\nGenerating and adding {count} random user(s)...\n")
    added, failed = [], []

    for i in range(count):
        user_data = generate_random_user()
        try:
            response = requests.post(f"{BASE_URL}/users/", json=user_data)
        except requests.exceptions.ConnectionError:
            print("Error: cannot connect to the API server. Start it with: uvicorn myapi:app --reload")
            sys.exit(1)

        if response.status_code == 201:
            created = response.json()
            added.append(created)
            print(f"[OK]   {i + 1}/{count}: #{created['id']} {created['name']} <{created['email']}> ({created['role']})")
        else:
            failed.append((user_data, response.text))
            print(f"[FAIL] {i + 1}/{count}: HTTP {response.status_code} {response.text[:200]}")

    print(f"\nSummary: added {len(added)}, failed {len(failed)}")
    if added:
        total = len(requests.get(f"{BASE_URL}/users/").json())
        print(f"Users in database: {total}")
    return len(failed) == 0


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    sys.exit(0 if add_random_users(count) else 1)
