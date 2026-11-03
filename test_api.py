"""
Smoke test against a running server (uvicorn myapi:app).
Every step checks the status code and the response body; the script exits with code 1 on the first failure.
Emails contain a random suffix, so the script can be run many times against the same database.

Usage:
    uvicorn myapi:app --reload        # in one terminal
    python test_api.py                # in another terminal
"""
import json
import sys
import uuid

import requests

BASE_URL = "http://127.0.0.1:8000"
RUN = uuid.uuid4().hex[:8]
passed = 0


def check(step, response, expected_status, predicate=None):
    """Assert the status code (and optionally the JSON body) and print a one-line result."""
    global passed
    try:
        body = response.json()
    except ValueError:
        body = response.text
    ok = response.status_code == expected_status and (predicate is None or predicate(body))
    mark = "OK  " if ok else "FAIL"
    print(f"[{mark}] {step}: HTTP {response.status_code} (expected {expected_status})")
    if not ok:
        print("       response:", json.dumps(body, ensure_ascii=False)[:300])
        sys.exit(1)
    passed += 1
    return body


def test_api():
    print(f"Running API smoke test against {BASE_URL} (run id {RUN})\n")
    check("GET / returns a message", requests.get(f"{BASE_URL}/"), 200, lambda b: "message" in b)

    users = {
        "jan": {"name": "Jan Kowalski", "email": f"jan.kowalski.{RUN}@example.com", "role": "admin"},
        "anna": {"name": "Anna Nowak", "email": f"anna.nowak.{RUN}@example.com", "role": "user"},
        "piotr": {"name": "Piotr Wiśniewski", "email": f"piotr.wisniewski.{RUN}@example.com", "role": "moderator"},
    }
    ids = {}
    for key, data in users.items():
        body = check(f"POST /users/ creates {data['name']}", requests.post(f"{BASE_URL}/users/", json=data), 201,
                     lambda b, d=data: b["email"] == d["email"] and isinstance(b["id"], int))
        ids[key] = body["id"]

    check("POST duplicate email is rejected", requests.post(f"{BASE_URL}/users/", json=users["jan"]), 400,
          lambda b: b["detail"] == "Email already registered")
    check("POST invalid email is rejected", requests.post(f"{BASE_URL}/users/", json={**users["jan"], "email": "not-an-email"}), 422)
    check("POST missing field is rejected", requests.post(f"{BASE_URL}/users/", json={"name": "No Email"}), 422)

    check("GET /users/ lists created users", requests.get(f"{BASE_URL}/users/"), 200,
          lambda b: {ids["jan"], ids["anna"], ids["piotr"]} <= {u["id"] for u in b})
    check("GET /users/{id} returns the user", requests.get(f"{BASE_URL}/users/{ids['jan']}"), 200,
          lambda b: b["name"] == "Jan Kowalski")

    full = {"name": "Anna Kowalska", "email": f"anna.kowalska.{RUN}@example.com", "role": "admin"}
    check("PUT full update", requests.put(f"{BASE_URL}/users/{ids['anna']}", json=full), 200,
          lambda b: b == {**full, "id": ids["anna"]})
    check("PUT partial update changes only role", requests.put(f"{BASE_URL}/users/{ids['piotr']}", json={"role": "super_admin"}), 200,
          lambda b: b["role"] == "super_admin" and b["name"] == "Piotr Wiśniewski")
    check("PUT to an email that is taken is rejected",
          requests.put(f"{BASE_URL}/users/{ids['piotr']}", json={"email": users["jan"]["email"]}), 400)
    check("PUT invalid email is rejected", requests.put(f"{BASE_URL}/users/{ids['piotr']}", json={"email": "bad"}), 422)

    check("GET unknown id returns 404", requests.get(f"{BASE_URL}/users/999999"), 404)
    check("GET non-numeric id returns 422", requests.get(f"{BASE_URL}/users/abc"), 422)

    for key in ids:
        check(f"DELETE user {ids[key]}", requests.delete(f"{BASE_URL}/users/{ids[key]}"), 200)
    check("GET deleted user returns 404", requests.get(f"{BASE_URL}/users/{ids['jan']}"), 404)
    check("DELETE unknown id returns 404", requests.delete(f"{BASE_URL}/users/999999"), 404)

    print(f"\nAll {passed} checks passed.")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\nError: cannot connect to the API server. Start it with: uvicorn myapi:app --reload")
        sys.exit(1)
