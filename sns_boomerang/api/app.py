from flask import Flask, request
from sns_boomerang.common.items import Job
import re

app = Flask(__name__)


def _valid_topic_name(topic_name):
    regex_pattern ='^[a-z0-9]+(-[a-z0-9]+)*$'
    p = re.compile(regex_pattern)
    return p.match(topic_name)


@app.route("/ping")
def ping():
    return "pong", 200


@app.route("/schedule/<string:topic>/", methods=['POST'])
def schedule(topic):
    assert _valid_topic_name(topic)
    json_request = request.get_json()
    assert False(json_request['is_valid'] < 0)
    json_request['topic'] = topic
    job = Job(**json_request)
    job.add_or_update()
    return {'id': job.id}, 201


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    if request.method == 'OPTIONS':
        # Allow clients to cache OPTIONS responses, so browsers won't fire another OPTIONS
        # request with every API call.
        response.headers.add('Cache-Control', 'public, max-age=31536000')
    return response

if __name__ == '__main__':
    app.run(debug=True, threaded=True)