import requests


def subset(a, b, present=[]):
    subset = all((k in a and a[k] == v) for k, v in b.items())
    present = all(key in a for key in present)
    return subset and present


def post_subset(url, json, expected_subset, present):
    r = requests.post(url, json=json)
    assert r.status_code == requests.codes.ok
    response_json = r.json()
    assert subset(response_json, expected_subset, present), response_json
    return response_json


def get(url, code, expected=None, dont_crack_json=False):
    r = requests.get(url)
    assert r.status_code == code
    if dont_crack_json:
        return None
    request_json = r.json()
    if expected:
        assert request_json == expected
    return request_json
