#!/usr/bin/env python3
"""basic babel setup"""
from flask import Flask, render_template, request
from flask_babel import Babel
from typing import Union


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
def get_locale() -> Union[str, None]:
    """
    select and return the best language match based on supported
    languages
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index() -> str:
    """handler for the / route"""
    return render_template("2-index.html")


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)