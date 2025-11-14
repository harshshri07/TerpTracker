# TerpTracker

An AWS-hosted web application that allows users to view, manage, and track their finances and spending habits. Built with Flask and DynamoDB, TerpTracker provides an intuitive interface for expense tracking with detailed analytics and visualizations.

## Features

- **User Authentication**: Secure sign-up and login system with password hashing
- **Expense Tracking**: Add expenses with categories, payment types, amounts, dates, and notes
- **Monthly Summaries**: View detailed expense summaries by month
- **Data Visualization**: Interactive pie charts showing expense distribution by category
- **Multiple Payment Types**: Track expenses by card, cash, mobile/virtual, bank, or other
- **Expense Categories**: Organize expenses into categories like groceries, utilities, gas, rent, food & dining, entertainment, travel, and more
- **DynamoDB Integration**: Scalable NoSQL database for storing user data and expenses
- **Local Development**: Full local development environment with Docker Compose

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: AWS DynamoDB (with local DynamoDB for development)
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Containerization**: Docker & Docker Compose
- **Build Tools**: Python setuptools, Make
- **Deployment**: AWS ECR, Gunicorn/Uvicorn workers

## Quick Start

1. Clone the repository and install dependencies
2. Build the package and start the development server
3. Access the application at `http://localhost:5000`

For complete setup instructions, see [SETUP.md](SETUP.md).

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- pip (Python package manager)

See [SETUP.md](SETUP.md) for detailed prerequisites and installation instructions.

## Project Structure

```
terptracker/
├── app.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── pyproject.toml                  # Project metadata and dependencies
├── setup.py                        # Package setup configuration
├── Dockerfile                      # Docker image configuration
├── docker-compose.yml              # Local DynamoDB services
├── Makefile                        # Build and run commands
│
├── terptracker/
│   ├── constants/
│   │   └── DynamoDbConstants.py   # DynamoDB configuration constants
│   │
│   ├── dynamodb/
│   │   ├── TerpTrackerDb.py        # Main database operations class
│   │   ├── dynamodb_helpers.py    # DynamoDB utility functions
│   │   └── tables/
│   │       ├── AppLoginTable.py   # User authentication table schema
│   │       └── ExpenseTable.py    # Expense tracking table schema
│   │
│   └── website/
│       ├── __init__.py             # Flask app factory
│       ├── auth.py                 # Authentication routes (login/signup)
│       ├── views.py                # Main application views
│       ├── models.py               # User model
│       ├── summary.py              # Expense summary and analytics routes
│       └── templates/
│           ├── base.html          # Base template
│           ├── login.html         # Login page
│           ├── sign_up.html       # Registration page
│           ├── home.html          # Expense entry form
│           ├── summary.html       # Summary selection page
│           ├── summary_table.html # Monthly expense table
│           └── pie_chart.html     # Expense visualization
```

## Development Setup

For detailed setup instructions, running commands, environment variables, and troubleshooting, see [SETUP.md](SETUP.md).

## Database Schema

### LOGIN Table
- **Partition Key**: `user_id` (String)
- **Global Secondary Index**: `username-index` on `email`
- **Attributes**: `user_id`, `email`, `firstName`, `password` (hashed)

### USER_EXPENSES Table
- **Partition Key**: `userEmail` (String)
- **Sort Key**: `expenseTimestamp` (String)
- **Global Secondary Index**: `UserTimestampIndex` on `userEmail` and `expenseTimestamp`
- **Attributes**: 
  - `userEmail`: User's email address
  - `expenseTimestamp`: Timestamp of the expense
  - `expenseType`: Payment type (card, cash, mobile_virtual, bank, other)
  - `expenseCategory`: Expense category
  - `expenseAmount`: Amount spent
  - `userNote`: Optional note about the expense

## Usage

1. **Sign Up**: Create a new account with your email and password
2. **Add Expenses**: Use the home page to add expenses with:
   - Payment type (card, cash, mobile/virtual, bank, other)
   - Category (groceries, utilities, gas, rent, food & dining, entertainment, travel, etc.)
   - Amount
   - Date
   - Optional note
3. **View Summaries**: Navigate to the summary page to view monthly expense breakdowns
4. **Visualize Data**: View pie charts showing expense distribution by category for any month

## Production Deployment

For production deployment, the application can be containerized using Docker and deployed to AWS:

1. Build the Docker image:
   ```bash
   docker build -t terptracker-app .
   ```

2. Set environment variables for production:
   - `DB_MODE=PROD`
   - `DYNAMODB_URL=<your-aws-dynamodb-endpoint>`
   - `AWS_ACCESS_KEY_ID=<your-access-key>`
   - `AWS_SECRET_ACCESS_KEY=<your-secret-key>`

3. Run with production server (Gunicorn):
   ```bash
   make terptracker-prod
   ```

## Contributing

This is a group project. When contributing:

1. Make your changes to the codebase
2. Rebuild the package and test locally
3. Commit and push your changes

For detailed development workflow and commands, see [SETUP.md](SETUP.md).

## License

MIT License

## Authors

MSML650 Final Project - TerpTracker Team
