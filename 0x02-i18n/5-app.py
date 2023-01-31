#!/usr/bin/env python3
"""basic babel setup"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """Configuration for Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

babel = Babel(app)

@babel.localeselector
def get_locale():
    """
    select and return the best language match based on supported languages
    """
    loc = request.args.get('locale')
    if loc in app.config['LANGUAGES']:
        return loc
    return request.accept_languages.best_match(app.config['LANGUAGES'])

def get_user() -> Union[Dict, None]:
    """
    function that returns a user dictionary or None if the ID cannot be found
    or if login_as was not passed
    """
    id = request.args.get('login_as', None)
    if id and int(id) in users:
        return users.get(int(id))
    return None

@app.before_request
def before_request() -> None:
    """
    find a user if any, and set it as a global on flask.g.user
    """
    user = get_user()
    g.user = user

@app.route('/')
def index() -> str:
    """handler for the / route"""
    return render_template("5-index.html")


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
