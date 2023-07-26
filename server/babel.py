import os
import subprocess
from flask import request, session, jsonify
from flask_babel import Babel


def get_languages_from_dir(directory):
    """Return a list of directory names in the given directory."""
    return [name for name in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, name))]


BABEL_DEFAULT_LOCALE = 'en_US'
BABEL_LANGUAGES = get_languages_from_dir('translations')


def create_babel(app):
    """Create and initialize a Babel instance with the given Flask app."""
    babel = Babel(app)
    app.config['BABEL_DEFAULT_LOCALE'] = BABEL_DEFAULT_LOCALE
    app.config['BABEL_LANGUAGES'] = BABEL_LANGUAGES

    babel.init_app(app, locale_selector=get_locale)
    compile_translations()


def get_locale():
    """Get the user's locale from the session or the request's accepted languages."""
    return session.get('language') or request.accept_languages.best_match(BABEL_LANGUAGES)


def get_languages():
    """Return a list of available languages in JSON format."""
    return jsonify(BABEL_LANGUAGES)


def compile_translations():
    """Compile the translation files."""
    result = subprocess.run(
        ['pybabel', 'compile', '-d', 'translations'],
        stdout=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise Exception(
            f'Compiling translations failed:\n{result.stdout.decode()}')

    print('Translations compiled successfully')
