from flask import Flask

from app.config import ProductionConfig, DevelopmentConfig

import os

## Extensions declaration ##
basedir = os.path.abspath(os.path.dirname(__file__))

## Application factory init ##
def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        print("Starting with ProductionConfig")
        app.config.from_object(ProductionConfig)
    else:
        print("Starting with DevelopmentConfig")
        app.config.from_object(DevelopmentConfig)

    app.url_map.strict_slashes = True

    init_extensions(app)

    # Adding the views
    from app.views.webpage import webpage

    app.register_blueprint(webpage)

    return app


## Init extensions
def init_extensions(app):
    # Init Flask-SQLAlchemy
    print('Init Flask extensions!')