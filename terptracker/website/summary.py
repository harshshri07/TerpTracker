from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user
from terptracker.dynamodb.TerpTrackerDb import TerpTrackerDb
from terptracker.constants.DynamoDbConstants import DynamoDbConstants
from terptracker.dynamodb.dynamodb_helpers import *
from boto3.dynamodb.conditions import Key, Attr
from collections import Counter
import random


summary = Blueprint('summary', __name__)

bsky_dynamodb = TerpTrackerDb(db_mode=DynamoDbConstants.DB_MODE)
db_resource = get_dynamodb_resource(db_mode=DynamoDbConstants.DB_MODE)
user_expenses_table = get_dynamodb_table(dynamodb_resource=db_resource,
                                         table_name=DynamoDbConstants.TERPTRACKER_USER_EXPENSES_TABLE_NAME)


def get_category_counts(posts):
    category_counter = Counter()
    for post in posts:
        for cat in post.get('category', []):
            category_counter[cat] += 1
    return category_counter


def generate_color_palette(n):
    base_colors = [
        "rgba(75, 192, 192, 0.5)",
        "rgba(255, 99, 132, 0.5)",
        "rgba(255, 206, 86, 0.5)",
        "rgba(54, 162, 235, 0.5)",
        "rgba(153, 102, 255, 0.5)",
        "rgba(255, 159, 64, 0.5)",
        "rgba(201, 203, 207, 0.5)"
    ]
    return [random.choice(base_colors) for _ in range(n)]


@summary.route('/summary', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        month_year = request.values.get('month')

        year = month_year.split('-')[0]
        month = month_year.split('-')[1]
        day = 0

        if month in ['01', '03', '05', '07', '08', '10', '12']:
            day = 31
        elif month == '02':
            is_leap_year = isLeapYear(year)
            if is_leap_year:
                day = 29
            else:
                day = 28
        else:
            day = 30

        start = get_first_timestamp_of_month(year=int(year), month=int(month))
        end = get_last_timestamp_of_month(year=int(year), month=int(month), day=day)

        response = user_expenses_table.query(
            IndexName='UserTimestampIndex',
            KeyConditionExpression=Key('userEmail').eq(current_user.email) & Key('expenseTimestamp').between(start, end)
        )

        norm_records = normalize_summary_records(response['Items'])
        return render_template("summary_table.html",
                               selected_month=month_year,
                               expenses=norm_records)
    else:
        return render_template('summary.html')

@summary.route('/pie_chart', methods=['GET', 'POST'])
@login_required
def get_pie_chart():
    if request.method == 'GET':
        month_year = request.values.get('month')
        print(f'{month_year=}')

        year = month_year.split('-')[0]
        month = month_year.split('-')[1]
        day = 0

        if month in ['01', '03', '05', '07', '08', '10', '12']:
            day = 31
        elif month == '02':
            is_leap_year = isLeapYear(year)
            if is_leap_year:
                day = 29
            else:
                day = 28
        else:
            day = 30

        start = get_first_timestamp_of_month(year=int(year), month=int(month))
        end = get_last_timestamp_of_month(year=int(year), month=int(month), day=day)

        response = user_expenses_table.query(
            IndexName='UserTimestampIndex',
            KeyConditionExpression=Key('userEmail').eq(current_user.email) & Key('expenseTimestamp').between(start, end)
        )

        norm_records = normalize_summary_records(response['Items'])
        return render_template("pie_chart.html",
                               selected_month=month_year,
                               expenses=norm_records)
