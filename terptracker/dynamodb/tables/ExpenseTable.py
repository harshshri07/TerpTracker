import botocore.exceptions
from terptracker.dynamodb.dynamodb_helpers import *
from terptracker.constants.DynamoDbConstants import DynamoDbConstants


class ExpenseTable:
    """
    Handles the dynamodb table schema used to create the USER_EXPENSES DynamoDB table.

    """

    def __init__(self, db_mode):
        """
        Initializes a USER_EXPENSES instance by making the DynamoDB resource and client objects readily available
        """
        self.dynamodb_resource = get_dynamodb_resource(db_mode=db_mode)
        self.dynamodb_client = get_dynamodb_client(db_mode=db_mode)

    def create_table(self):
        """
        Creates a USER_EXPENSES DynamoDB table with the necessary schema and a global secondary index.

        The table uses 'bskyUsername' as the partition key and 'bskyPostHash' as the sort key.
        The schema also defines a global secondary index on 'timelineDate' to support queries by date.

        Returns:
            None
        """
        try:
            expense_table_exists = table_exists(client=self.dynamodb_client,
                                              table_name=DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME)
            if expense_table_exists is True:
                print(f'✅{DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME} table already exists')
                return
            else:
                print(f'🚧Creating {DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME}...')
                table = self.dynamodb_resource.create_table(
                    TableName=DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME,
                    KeySchema=[
                        {
                            'AttributeName': 'userEmail',
                            'KeyType': 'HASH'  # Partition key
                        },
                        {
                            'AttributeName': 'expenseTimestamp',
                            'KeyType': 'RANGE'  # Sort key
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'userEmail',
                            'AttributeType': 'S'
                        },
                        {
                            'AttributeName': 'expenseTimestamp',
                            'AttributeType': 'S'
                        },
                    ],
                    BillingMode='PAY_PER_REQUEST',
                    GlobalSecondaryIndexes=[
                        {
                            'IndexName': 'UserTimestampIndex',
                            'KeySchema': [
                                {
                                    'AttributeName': 'userEmail',
                                    'KeyType': 'HASH'
                                },
                                {
                                    'AttributeName': 'expenseTimestamp',
                                    'KeyType': 'RANGE'
                                }
                            ],
                            'Projection': {
                                'ProjectionType': 'ALL',
                            }
                        }
                    ]
                )
                table.wait_until_exists()
                print(f"✅{DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME} table created successfully.")

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print(f"⚠️ {DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME} is being created by another process. Skipping.")
            else:
                print(f'🚨DynamoDB error when trying to create {DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME} table: {e}')
