import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config["DATABASE"] = "dev.db"

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import db
        db.init_app(app)

    from . import transactions
    app.register_blueprint(transactions.blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
