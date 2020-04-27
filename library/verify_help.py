import requests
from deepdiff import DeepDiff


class IncorrectCodeError(Exception):

    def __init__(self, path, actual, expected):
        self.path = path
        self.expected = expected
        self.actual = actual

    def __repr__(self):
        return "Assertion failed for: %s, status_code recvd: %s, expected: %s" % (self.path, self.actual, self.expected)

    def __str__(self):
        return "Assertion failed for: %s, status_code recvd: %s, expected: %s" % (self.path, self.actual, self.expected)


def compare_keys(dict_with_keys, other):
    returned = []
    for k, v in dict_with_keys.items():
        if v != other[k] and str(v) != str(other[k]):
            returned.append((k, v, other[k]))
    return returned


def test_post_url(path, post_data=None, code=requests.codes.ok, expected=None, cookies=None, s=None, test_for_cors=False):
    if s:
        r = s.post(path, json=post_data, cookies=cookies)
    else:
        r = requests.post(path, json=post_data, cookies=cookies)
    if r.status_code != code:
        raise IncorrectCodeError(path, r.status_code, code)
    # assert r.status_code == code, "Assertion failed for: %s, status_code recvd: %s, expected: %s" % (path, r.status_code, code)
    if test_for_cors:
        assert r.headers['Access-Control-Allow-Origin'] == '*'
    try:
        request_json = r.json()
        if expected:
            assert request_json == expected
        return request_json
    except AssertionError as ae:
        raise ae
    except Exception:
        return None


def test_put_url(path, post_data=None, code=requests.codes.ok, expected=None, cookies=None, s=None):
    if s:
        r = s.put(path, json=post_data, cookies=cookies)
    else:
        r = requests.put(path, json=post_data, cookies=cookies)
    assert r.status_code == code, "Assertion failed for: %s, status_code recvd: %s, expected: %s" % (path, r.status_code, code)
    request_json = None
    try:
        request_json = r.json()
    except Exception:
        pass
    if expected:
        assert request_json == expected
    return request_json


def test_get_url(path, code=requests.codes.ok, json=None, expected=None, cookies=None, s=None, crack_json=False, ignore_keys=None):
    if s:
        r = s.get(path, json=json, cookies=cookies)
    else:
        r = requests.get(path, json=json, cookies=cookies)
    assert r.status_code == code, "Assertion failed for: %s, status_code recvd: %s, expected: %s" % (path, r.status_code, code)
    if expected is not None:
        request_json = r.json()
        if not ignore_keys:
            assert request_json == expected, "request_json=%s,\n expected=%s \n%s" % (str(request_json), str(expected), str(DeepDiff(request_json, expected)))
        else:
            diff = compare_keys(dict_with_keys=expected, other=request_json)
            assert diff == [], diff
        return request_json
    if crack_json:
        request_json = r.json()
        return request_json
