import datetime
import json

from flask import request, abort, Response, current_app

from library import app, db
from library.models import Request
from email_validator import validate_email, EmailNotValidError


def request_to_json(r):
    return {
        "id": r.id,
        "email": r.email,
        "title": r.title,
        "timestamp": r.timestamp
    }

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@app.route('/request', methods=['GET', 'POST'])
def request_route():
    if request.method == 'POST':
        content = request.json
        if content is None:
            abort(400)

        try:
            v = validate_email(content['email'])
            email = v["email"]
        except EmailNotValidError as e:
            abort(Response(json.dumps({'error':str(e)}), status=400))

        r = Request(email=email, title=content['title'])
        db.session.add(r)
        db.session.commit()
        return request_to_json(r)
    else:
        page = request.args.get('page', 1, type=int)
        all_requests = Request.query.order_by(Request.timestamp.desc()).paginate(page=page, per_page=current_app.config['PAGINATION_PER_PAGE'])

        return Response(json.dumps([request_to_json(r) for r in all_requests.items], default=myconverter),  mimetype='application/json')


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
