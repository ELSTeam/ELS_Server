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
        assert res.status_code == 400

    # positive test - user does exist
    payload["username"] = "omerap12"
    payload["password"] = "Aa123456!"
    res = requests.post(url, json=payload, headers=headers)
    assert res.status_code == 200


def sign_up(url):
    """
    Function purpose - check if the sign up of function works in server side at /sign_up
    """
    # user already exist
    payload = {"username": "omerap12", "password": "password"}
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url, json=payload, headers=headers)
    assert res.status_code == 400

    # user sign up successfully
    payload["username"] = "test_user"
    payload["password"] = "test_password"
    res = requests.post(url, json=payload, headers=headers)
    assert res.status_code == 200


def delete_user(url):
    """
    Function purpose - check for deleting user in server side at /delete
    """
    payload = {"username": "test_user", "password": "test_password"}
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url, json=payload, headers=headers)
    assert res.status_code == 200


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 server_test.py [url]")
        exit(1)
    print("Checking sign in")
    check_sign_in(sys.argv[1] + '/sign_in')
    print("Passed")

    print("Checking sign up")
    sign_up(sys.argv[1] + '/sign_up')
    print("Passed")

    print("Checking delete user")
    delete_user(sys.argv[1] + '/delete')
    print("Passed")
