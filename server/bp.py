from flask import Blueprint

bp = Blueprint('bp', __name__,
               template_folder='./../client/html',
               static_folder='./../client',
               static_url_path='assets')
