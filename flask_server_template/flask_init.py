from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError, Schema, fields, validate
import logging
import os

db_obj = SQLAlchemy()

log = logging.getLogger('pythonLogger') # This handler comes from config>logger.conf
# https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/

def create_app(flask_config=None):
    """Construct the core application."""
    log.info(flask_config)
    app = Flask(__name__, instance_relative_config=False)

    if flask_config is None:
        app.config['DEBUG'] = False
        if 'SQLALCHEMY_DATABASE_URI' not in os.environ:
            raise RuntimeError('Environment variables not set')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = False
    else:
        app.config.from_object(flask_config)

    db_obj.init_app(app)

    with app.app_context():
        # Import routes
        import flask_routes
        return app


'''To validate the input parameters'''
def some_custom_check(data):
    '''can be replaced with customized check'''
    if not data:
        raise ValidationError('some_custom_check for title failed')
class TitleValidator(Schema):
    '''https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html'''
    title = fields.Str(required=True, validate=[validate.Length(min=1, max=50), some_custom_check])


