import requests


# post a request with no json body
from library.test.test_help import post_subset, get

r = requests.post('http://localhost:5000/request')
assert r.status_code == requests.codes.bad


# post a request with bad json
r = requests.post('http://localhost:5000/request', data='{"data":"notgood}"')
assert r.status_code == requests.codes.bad


# post a request with bad email
request0 = {"email": "@email.com", "title": "good title"}
r = requests.post('http://localhost:5000/request', json=request0)
assert r.status_code == requests.codes.bad
assert r.json()['error'] == 'There must be something before the @-sign.'


# post a good request
request1 = {"email": "good@email.com", "title": "good title"}
response1 = post_subset('http://localhost:5000/request', request1, request1, ["id", "timestamp"])


# get a specific request
get('http://localhost:5000/request/%s' % response1['id'],
             code=requests.codes.ok, expected=response1)


# get a specific request that shouldn't be there
get('http://localhost:5000/request/36000',
             code=requests.codes.not_found, dont_crack_json=True)


# get all requests and check that the one we just created is there
response_json = get('http://localhost:5000/request', requests.codes.ok)
assert response1['id'] in [r['id'] for r in response_json]


# delete the request just created
r = requests.delete('http://localhost:5000/request/%s' % response1['id'])
assert r.status_code == requests.codes.no_content


# get all requests and check the one we just created is not there
response_json = get('http://localhost:5000/request', requests.codes.ok)
assert response1['id'] not in [r['id'] for r in response_json]


# delete a request that doesn't exist
r = requests.delete('http://localhost:5000/request/%s' % response1['id'])
assert r.status_code == requests.codes.not_found


# test for pagination
for i in range(0,21):
    request1 = {"email": "good@email.com", "title": "title %s"%i}
    post_subset('http://localhost:5000/request', request1, request1, ["id", "timestamp"])
page_1 = get('http://localhost:5000/request', requests.codes.ok)
assert len(page_1) == 20, len(response_json)
# text next page is different to page_1
page_2 = get('http://localhost:5000/request?page=2', requests.codes.ok)
for id in [r['id'] for r in page_2]:
    assert id not in (p1r['id'] for p1r in page_1)
