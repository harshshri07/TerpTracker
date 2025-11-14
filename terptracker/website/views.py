from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from terptracker.dynamodb.TerpTrackerDb import TerpTrackerDb
from terptracker.dynamodb.dynamodb_helpers import *
from terptracker.constants.DynamoDbConstants import DynamoDbConstants
from datetime import datetime, date, timezone
from .models import User
from boto3.dynamodb.conditions import Key
import requests
import json

views = Blueprint('views', __name__)

bsky_dynamodb = TerpTrackerDb(db_mode=DynamoDbConstants.DB_MODE)
db_resource = get_dynamodb_resource(db_mode=DynamoDbConstants.DB_MODE)
user_expenses_table = get_dynamodb_table(dynamodb_resource=db_resource,
                                         table_name=DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME)


def timestamp_with_current_time(year: int, month: int, day: int):
    """
    Build a UTC-aware datetime for the given calendar date using the current
    UTC time-of-day.

    Returns (utc datetime object, epoch_seconds_float).
    """
    now_utc = datetime.now(timezone.utc)  # current time in UTC
    dt = datetime.combine(date(year, month, day),  now_utc.timetz())
    return dt, dt.timestamp()


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        try:
            expense_type = request.form.get('expense_type')
            expense_category = request.form.get('expense_category')
            expense_amount = request.form.get('expense_amount')
            expense_date = request.form.get('expense_date')
            user_note = request.form.get('expense_note')

            year = int(expense_date.split('-')[0])
            month = int(expense_date.split('-')[1])
            day = int(expense_date.split('-')[2])

            dt, epoch = timestamp_with_current_time(year=year, month=month, day=day)
            user_expense_item = {'userEmail': current_user.email, 'expenseTimestamp': str(epoch),
                                 'expenseType': expense_type, 'expenseCategory': expense_category,
                                 'expenseAmount': expense_amount, 'userNote': user_note}

            user_expenses_table.put_item(Item=user_expense_item)
            flash(f'Successfully added your {expense_category} expense')

        except Exception as e:
            print(e)
            flash('There was an error parsing your information', category='error')

    return render_template("home.html")


@views.route('/task_status/<task_id>')
@login_required
def task_status_page(task_id):
    return render_template('task_status.html', task_id=task_id)


@views.route('/health', methods=['GET'])
def health():
    return "Healthy!", 200
