import os

from flask import Flask, request, render_template, redirect, url_for, session, g

import models
from database import engine, SessionLocal


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'pwp_db.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    models.Base.metadata.create_all(bind=engine)

    import database
    database.init_app(app)

    import auth
    app.register_blueprint(auth.bp)

    import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='home')

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('page_not_found.html'), 404

    @app.route('/')
    def home():
        if g.user is None:
            return redirect(url_for('auth.login'))
        else:
            return render_template('home.html')

    return app
