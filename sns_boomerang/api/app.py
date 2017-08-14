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


if __name__ == '__main__':
    app.run()
