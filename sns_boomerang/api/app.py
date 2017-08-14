from flask import Flask
from sns_boomerang.api.resources import api

app = Flask(__name__)
api.init_app(app)


@app.route("/ping")
def ping():
    return "pong", 200


if __name__ == '__main__':
    app.run()
