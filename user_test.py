import os
import re
import requests

BASE_URL = os.getenv("BASE_URL", "https://ghans.me")

EMAIL = os.getenv("TEST_EMAIL")
PASSWORD = os.getenv("TEST_PASSWORD")

session = requests.Session()


def get_csrf(url):
    response = session.get(url, timeout=10)
    response.raise_for_status()

    match = re.search(
        r'name="csrfmiddlewaretoken" value="(.+?)"',
        response.text
    )

    if not match:
        raise ValueError(f"CSRF token not found: {url}")

    return match.group(1)


def register():
    csrf = get_csrf(f"{BASE_URL}/register/")

    payload = {
        "csrfmiddlewaretoken": csrf,
        "email": EMAIL,
        "password1": PASSWORD,
        "password2": PASSWORD,
        "first_name": "Test",
        "last_name": "User",
        "consent_given": "on",
    }

    response = session.post(
        f"{BASE_URL}/register/",
        data=payload,
        timeout=10
    )

    response.raise_for_status()

    if "verify-otp" not in response.url:
        raise RuntimeError("Registration failed")

    user_id = response.url.split("/")[-2]
    return user_id


def verify_otp(user_id, otp):
    csrf = get_csrf(
        f"{BASE_URL}/verify-otp/{user_id}/"
    )

    payload = {
        "csrfmiddlewaretoken": csrf,
        "otp": otp,
    }

    response = session.post(
        f"{BASE_URL}/verify-otp/{user_id}/",
        data=payload,
        timeout=10
    )

    response.raise_for_status()


def login():
    csrf = get_csrf(f"{BASE_URL}/my-login/")

    payload = {
        "csrfmiddlewaretoken": csrf,
        "username": EMAIL,
        "password": PASSWORD,
    }

    response = session.post(
        f"{BASE_URL}/my-login/",
        data=payload,
        timeout=10
    )

    response.raise_for_status()

    return "client-dashboard" in response.url


def test_dashboard():
    response = session.get(
        f"{BASE_URL}/client/client-dashboard/",
        timeout=10
    )

    response.raise_for_status()
    return response.status_code == 200


if __name__ == "__main__":
    if not EMAIL or not PASSWORD:
        raise ValueError(
            "Set TEST_EMAIL and TEST_PASSWORD environment variables."
        )

    print("Authentication test script loaded.")