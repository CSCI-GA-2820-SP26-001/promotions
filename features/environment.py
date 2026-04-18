"""
Environment setup for BDD tests
"""
from wsgi import app
from service.models import db, Promotion


def before_all(context):
    """Run once before all tests"""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
    context.app = app
    context.app_context = app.app_context()
    context.app_context.push()
    context.client = app.test_client()
    db.create_all()


def after_all(context):
    """Run once after all tests"""
    db.session.close()
    context.app_context.pop()


def before_scenario(context, scenario):
    """Run before each scenario - clear the database"""
    db.session.query(Promotion).delete()
    db.session.commit()


def after_scenario(context, scenario):
    """Run after each scenario"""
    db.session.remove()