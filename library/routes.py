from flask import request, abort

from library import app, db
from library.models import Request


def request_to_json(r):
    return {
        "id": r.id,
        "email": r.email,
        "title": r.title,
        "timestamp": r.timestamp
    }


@app.route('/request', methods=['GET', 'POST'])
def request_route():
    if request.method == 'POST':
        content = request.json
        if content is None:
            abort(400)
        print(content)
        r = Request(email=content['email'], title=content['title'])
        db.session.add(r)
        db.session.commit()
        return request_to_json(r)
    else:
        all_requests = Request.query.all()
        return {"all_requests": [request_to_json(r) for r in all_requests]}


@app.route("/request/<int:request_id>", methods=['GET'])
def one_request_route(request_id):
    r = Request.query.get_or_404(request_id)
    return request_to_json(r)


@app.route("/request/<int:request_id>", methods=['DELETE'])
def delete_request_route(request_id):
    r = Request.query.get_or_404(request_id)
    db.session.delete(r)
    db.session.commit()
    return ('', 204)
