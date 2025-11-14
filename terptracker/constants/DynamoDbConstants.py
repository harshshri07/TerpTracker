import os


class DynamoDbConstants:
    TERPTRACKER_LOGIN_TABLE_NAME = 'LOGIN'
    TERPTRACKER_USER_EXPENSES_TABLE_NAME = 'USER_EXPENSES'
    DYNAMODB_REGION = 'us-east-1'
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY_ID = os.getenv('AWS_SECRET_ACCESS_KEY')
    DYNAMODB_URL = os.getenv('DYNAMODB_URL', 'http://localhost:8000')
    DYNAMODB_DEV_URL = 'http://localhost:8000'
    DB_MODE = os.getenv('DB_MODE', 'DEV')
    FERNET_KEY = 'FERNET_KEY'
