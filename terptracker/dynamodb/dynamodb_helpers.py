import boto3
import uuid
import os
from terptracker.constants.DynamoDbConstants import DynamoDbConstants
from datetime import datetime, date, timezone


def get_dynamodb_resource(db_mode: str):
    """
    Returns a boto3 DynamoDB resource configured for the given environment.

    Args:
        db_mode (str): Deployment mode. Use 'PROD' for production; otherwise, development settings are used.

    Returns:
        boto3.resources.factory.dynamodb.ServiceResource: A DynamoDB resource object.
    """
    if db_mode.upper() == 'PROD':
        return boto3.resource(
            'dynamodb',
            region_name=DynamoDbConstants.DYNAMODB_REGION,
            aws_access_key_id=DynamoDbConstants.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=DynamoDbConstants.AWS_SECRET_ACCESS_KEY_ID
        )
    elif db_mode.upper() == 'DEV':
        return boto3.resource(
            'dynamodb',
            region_name=DynamoDbConstants.DYNAMODB_REGION,
            aws_access_key_id='dummy',
            aws_secret_access_key='dummy',
            endpoint_url=DynamoDbConstants.DYNAMODB_URL
        )


def get_dynamodb_client(db_mode: str):
    """
    Returns a low-level boto3 DynamoDB client configured for the given environment.

    Args:
        db_mode (str): Deployment mode. Use 'PROD' for production; otherwise, development settings are used.

    Returns:
        botocore.client.DynamoDB: A DynamoDB client object.
    """
    if db_mode.upper() == 'PROD':
        return boto3.client(
            'dynamodb',
            region_name=DynamoDbConstants.DYNAMODB_REGION,
            aws_access_key_id=DynamoDbConstants.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=DynamoDbConstants.AWS_SECRET_ACCESS_KEY_ID
        )
    elif db_mode.upper() == 'DEV':
        return boto3.client(
            'dynamodb',
            region_name=DynamoDbConstants.DYNAMODB_REGION,
            aws_access_key_id='dummy',
            aws_secret_access_key='dummy',
            endpoint_url=DynamoDbConstants.DYNAMODB_URL
        )


def get_dynamodb_table(dynamodb_resource: boto3.resource, table_name: str):
    """
    Retrieves a reference to a DynamoDB table by name using a provided resource.

    Args:
        dynamodb_resource (boto3.resource): The DynamoDB resource object.
        table_name (str): The name of the table to access.

    Returns:
        boto3.dynamodb.Table: The table object reference.
    """
    table = dynamodb_resource.Table(table_name)
    return table


def table_exists(client: boto3.client, table_name: str):
    """
    Checks whether a DynamoDB table exists.

    Args:
        client (boto3.client): The DynamoDB client object.
        table_name (str): The name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    exists = False
    tables = client.list_tables()

    if table_name in tables['TableNames']:
        exists = True

    return exists


def stable_hash(input: str):
    """
    Generates a deterministic UUID based on the input string using UUIDv5.

    Args:
        input (str): The input string to hash (e.g., post text).

    Returns:
        str: A UUIDv5-based hash string.
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, input))


def timestamp_with_current_time(year: int, month: int, day: int):
    """
    Build a UTC-aware datetime for the given calendar date using the current
    UTC time-of-day.

    Returns (utc datetime object, epoch_seconds_float).
    """
    now_utc = datetime.now(timezone.utc)  # current time in UTC
    dt = datetime.combine(date(year, month, day),  now_utc.timetz())
    return dt, dt.timestamp()


def normalize_summary_records(response: list):
    norm_records = []
    for r in response:
        norm_record = r.copy()
        norm_record['expenseAmount'] = float(norm_record['expenseAmount'])
        norm_record['expenseTimestamp'] = float(norm_record['expenseTimestamp'])
        norm_record['date_str'] = (datetime.fromtimestamp(norm_record['expenseTimestamp'], tz=timezone.utc).date()
                                   .isoformat())
        norm_records.append(norm_record)
    return norm_records

def isLeapYear(year):
    # Check if n is divisible by 4
    if year % 4 == 0:
        # If it's divisible by 100, it should also be divisible by 400 to be a leap year
        if year % 100 == 0:
            return year % 400 == 0
        return True
    return False


def get_first_timestamp_of_month(year: int, month: int):
    start = datetime(year=year, month=month, day=1,
                     hour=0, minute=0, second=0, microsecond=0,
                     tzinfo=timezone.utc)
    return str(start.timestamp())


def get_last_timestamp_of_month(year: int, month: int, day: int):
    end = datetime(year=year, month=month, day=day,
                   hour=23, minute=59, second=59, microsecond=999_999,
                   tzinfo=timezone.utc)
    return str(end.timestamp())
