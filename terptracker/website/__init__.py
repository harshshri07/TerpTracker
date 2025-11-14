import boto3
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_session import Session
from terptracker.dynamodb.TerpTrackerDb import TerpTrackerDb
from terptracker.dynamodb.dynamodb_helpers import (table_exists, DynamoDbConstants, get_dynamodb_resource,
                                                  get_dynamodb_client, get_dynamodb_table)
import redis

# db = SQLAlchemy()
# DB_NAME = "database.db"
db_resource = get_dynamodb_resource(db_mode=DynamoDbConstants.DB_MODE)
db_client = get_dynamodb_client(db_mode=DynamoDbConstants.DB_MODE)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'terptracker_msml'

    app.config['SESSION_PERMANENT'] = False  # Optional: make session expire on browser close

    from .views import views
    from .auth import auth
    from .summary import summary

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(summary, url_prefix='/')

    from .models import User

    # with app.app_context():
    #     db.create_all()
    # create_database(app=app, db=db)
    bsky_dynamodb = TerpTrackerDb(db_mode=DynamoDbConstants.DB_MODE)
    print('Initializing TerpTracker Database...')

    login_table_exists = table_exists(client=db_client, table_name=DynamoDbConstants.TERPTRACKER_LOGIN_TABLE_NAME)
    if login_table_exists is False:
        bsky_dynamodb.create_login_table()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    login_table = get_dynamodb_table(dynamodb_resource=db_resource,
                                     table_name=DynamoDbConstants.TERPTRACKER_LOGIN_TABLE_NAME)

    @login_manager.user_loader
    def load_user(user_id):
        response = login_table.get_item(Key={'user_id': user_id})
        item = response.get('Item')
        if item:
            return User(user_id=item['user_id'], email=item['email'],first_name=item['firstName'], password_hash=item['password'])
        return None

    user_expenses_table_exists = table_exists(client=bsky_dynamodb.client, table_name=DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME)
    if user_expenses_table_exists is False:
        bsky_dynamodb.create_user_expenses_table()

    @app.context_processor
    def inject_user():
        from flask_login import current_user
        return dict(user=current_user)

    return app


def create_database(app, db):
    with app.app_context():
        db.create_all()
    # if not path.exists('website/' + DB_NAME):
    #     db.create_all()
    print('Created Database!')
