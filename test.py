#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get one user
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/users")
    r_j = r.json()
    user_id = r_j[0].get('id')

    """ PUT /api/v1/users/<user_id>
    """
    r = requests.put("http://0.0.0.0:5000/api/v1/users/{}".format(user_id), data={ 'first_name': "NewFirstName" }, headers={ 'Content-Type': "application/x-www-form-urlencoded" })
    print(r.status_code)
