"""The heckbot server."""

import random
import os

import flask


# Setup the flask app.
app = flask.Flask(__name__)


@app.route('/')
def root():
  print __name__(flask.request)
  return flask.render_template('index.html')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8585)
