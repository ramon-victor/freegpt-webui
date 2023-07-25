from flask import request, session, jsonify
from flask_babel import Babel

BABEL_DEFAULT_LOCALE = 'en_US'
BABEL_LANGUAGES = [
    'en_US',
    'es_MX',
    'pt_BR',
    'ru_RU',
    'zh_CN',
    'zh_TW',
    'fr_FR',
    'de_DE',
    'it_IT',
    'ja_JP',
    'ko_KR',
    'ar_SA',
    'hi_IN',
    'tr_TR',
]


def create_babel(app):
    """Create and initialize a Babel instance with the given Flask app."""
    babel = Babel(app)
    app.config['BABEL_DEFAULT_LOCALE'] = BABEL_DEFAULT_LOCALE
    app.config['BABEL_LANGUAGES'] = BABEL_LANGUAGES

    babel.init_app(app, locale_selector=get_locale)


def get_locale():
    """Get the user's locale from the session or the request's accepted languages."""
    user_language = session.get('language')
    if user_language is not None:
        return user_language

    return request.accept_languages.best_match(BABEL_LANGUAGES)


def get_languages():
    return jsonify(BABEL_LANGUAGES)
