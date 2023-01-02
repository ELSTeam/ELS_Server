import sys
import requests
import pytest


def check_sign_in(url):
    """
    Function purpose - check if the sign in function works in server side at /sign_in
    """
    # negative tests - user does not exist
    user_names = ["omer", "avital", "test", "nana"]
    passwords = ["1234", "Aa12345678!", "password", "wrong"]
    payload = {"username": None, "password": None}
    headers = {'Content-Type': 'application/json'}
    tuples = []
    for name in user_names:
        for password in passwords:
            tuples.append((name, password))

    for pair in tuples:
        payload["username"] = pair[0]
        payload["password"] = pair[1]
        res = requests.post(url, json=payload, headers=headers)
        # Todo - check this assert
        assert res.status_code == 400

    # positive test - user does exist
    payload["username"] = "omerap12"
    payload["password"] = "Aa123456!"
    res = requests.post(url, json=payload, headers=headers)
    # Todo - check this assert
    assert res.status_code == 200


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 server_test.py [url]")
        exit(1)
    check_sign_in(sys.argv[1]+'/sign_in')
