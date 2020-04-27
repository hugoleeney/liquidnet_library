from library.verify_help import test_post_url, test_get_url
import requests


def subset(a, b, present = []):
    subset = all((k in a and a[k]==v) for k,v in b.items())
    present = all(key in a for key in present)
    return subset and present


# post a request with no json body
test_post_url('http://localhost:5000/request', post_data=None, code=requests.codes.bad)


# post a request with bad json
r = requests.post('http://localhost:5000/request', data='{"data":"notgood}"')
assert r.status_code == requests.codes.bad


# post a good request
request1 = {"email":"good@email.com", "title": "good title"}
r = requests.post('http://localhost:5000/request', json=request1)
assert r.status_code == requests.codes.ok
response_json = r.json()
assert subset(response_json, request1, ["id", "timestamp"]), response_json
request1_id = response_json['id']


# get a specific request
test_get_url('http://localhost:5000/request/%s'%request1_id,
             code=requests.codes.ok, expected=response_json)


# get a specific request that shouldn't be there
test_get_url('http://localhost:5000/request/36000',
             code=requests.codes.not_found)


# get all requests and check that the one we just created is there
r = requests.get('http://localhost:5000/request')
assert r.status_code == requests.codes.ok
response_json = r.json()['all_requests']
assert request1_id in [r['id'] for r in response_json]


# delete the request just created
r = requests.delete('http://localhost:5000/request/%s'%request1_id)
assert r.status_code == requests.codes.no_content


# get all requests and check the one we just created is not there
r = requests.get('http://localhost:5000/request')
assert r.status_code == requests.codes.ok
response_json = r.json()['all_requests']
assert request1_id not in [r['id'] for r in response_json]


# delete a request that doesn't exist
r = requests.delete('http://localhost:5000/request/%s'%request1_id)
assert r.status_code == requests.codes.not_found
