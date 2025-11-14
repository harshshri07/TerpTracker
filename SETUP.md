# TerpTracker Setup Guide

This guide will walk you through setting up TerpTracker on your local machine for development.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

- **Python 3.8 or higher**
  - Check your version: `python --version` or `python3 --version`
  - Download from [python.org](https://www.python.org/downloads/) if needed

- **Docker Desktop** (for local DynamoDB)
  - Download from [docker.com](https://www.docker.com/products/docker-desktop/)
  - Ensure Docker is running before starting the application

- **pip** (Python package manager)
  - Usually comes with Python, but can be installed separately if needed

### Optional Tools

- **make** (for Linux/Mac users)
  - Most Linux distributions include `make` by default
  - On macOS, install via Xcode Command Line Tools: `xcode-select --install`
  - Windows users can use PowerShell commands instead (see below)

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/harshshri07/TerpTracker.git
cd TerpTracker
```

### 2. Install Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or if you prefer using a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Build the Python Package

You need to build and install the package locally:

**Linux/Mac:**
```bash
make build
```

**Windows (PowerShell):**
```powershell
python -m build
pip install .
```

This step needs to be repeated whenever you make code changes to the `terptracker` package.

## Running the Application

To run the app, you need to:
1. Build the Python package (once per code change)
2. Start the local DynamoDB containers
3. Launch the Flask development server

### Option 1: Using Make (Linux/Mac)

**First time setup:**
```bash
make build
```

**Start the development server:**
```bash
make terptracker-dev
```

This single command will:
- Stop any existing DynamoDB containers
- Start DynamoDB Local and DynamoDB Admin containers
- Set the `DB_MODE` environment variable to `DEV`
- Build and install the package
- Launch the Flask development server

### Option 2: Using PowerShell (Windows)

**Step 1: Build the package**
```powershell
python -m build
pip install .
```

**Step 2: Start DynamoDB containers**
```powershell
# Stop any existing containers
docker compose down --remove-orphans dynamodb-local dynamodb

# Start DynamoDB containers
docker compose up -d --remove-orphans dynamodb-local dynamodb
```

**Step 3: Set environment variable and run Flask**
```powershell
# Set environment variable
$env:DB_MODE="DEV"

# Build and install package (if you haven't already)
python -m build
pip install .

# Launch Flask dev server
python -m flask run --host=0.0.0.0 --port=5000
```

### Option 3: Manual Step-by-Step (All Platforms)

If you prefer to run each step manually:

1. **Start DynamoDB containers:**
   ```bash
   docker compose up -d --remove-orphans dynamodb-local dynamodb
   ```

2. **Set environment variable:**
   ```bash
   # Linux/Mac
   export DB_MODE=DEV
   
   # Windows PowerShell
   $env:DB_MODE="DEV"
   
   # Windows CMD
   set DB_MODE=DEV
   ```

3. **Build and install package:**
   ```bash
   python -m build
   pip install .
   ```

4. **Run Flask:**
   ```bash
   python -m flask run --host=0.0.0.0 --port=5000
   ```

## Accessing the Application

Once the server is running, you can access:

- **TerpTracker Application**: `http://localhost:5000`
- **DynamoDB Local**: `http://localhost:8000`
- **DynamoDB Admin UI**: `http://localhost:8001` (useful for viewing and managing local DynamoDB tables)

## Environment Variables

The application uses the following environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DB_MODE` | Database mode: `DEV` for local, `PROD` for AWS | `DEV` | No |
| `DYNAMODB_URL` | DynamoDB endpoint URL | `http://localhost:8000` | No (DEV mode) |
| `AWS_ACCESS_KEY_ID` | AWS access key | - | Yes (PROD mode) |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | - | Yes (PROD mode) |
| `FLASK_MODE` | Flask mode: `DEV` or `PROD` | `DEV` | No |

### Setting Environment Variables

**Linux/Mac:**
```bash
export DB_MODE=DEV
export DYNAMODB_URL=http://localhost:8000
```

**Windows PowerShell:**
```powershell
$env:DB_MODE="DEV"
$env:DYNAMODB_URL="http://localhost:8000"
```

**Windows CMD:**
```cmd
set DB_MODE=DEV
set DYNAMODB_URL=http://localhost:8000
```

For persistent environment variables, you can:
- Create a `.env` file in the project root (if using python-dotenv)
- Set them in your shell profile (`.bashrc`, `.zshrc`, etc.)
- Use your IDE's environment variable configuration

## Development Workflow

### Making Code Changes

1. **Edit your code** in the `terptracker/` directory
2. **Rebuild the package:**
   ```bash
   # Linux/Mac
   make build
   
   # Windows
   python -m build
   pip install .
   ```
3. **Restart the Flask server** (if it's running, stop it with `Ctrl+C` and restart)

### Stopping the Application

- **Stop Flask server**: Press `Ctrl+C` in the terminal running Flask
- **Stop DynamoDB containers:**
  ```bash
  docker compose down dynamodb-local dynamodb
  ```

### Viewing Local Database

Access the DynamoDB Admin UI at `http://localhost:8001` to:
- View all tables
- Inspect table items
- Query and scan tables
- Manage local DynamoDB data

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Rebuild the package after making changes:
```bash
python -m build
pip install .
```

### Issue: Docker containers won't start

**Solution:** 
- Ensure Docker Desktop is running
- Check if ports 8000 and 8001 are already in use
- Try stopping existing containers: `docker compose down`

### Issue: "Port 5000 already in use"

**Solution:**
- Find and stop the process using port 5000
- Or change the Flask port: `python -m flask run --host=0.0.0.0 --port=5001`

### Issue: DynamoDB tables not created

**Solution:**
- Tables are created automatically on first run
- Check Docker logs: `docker compose logs dynamodb-local`
- Ensure `DB_MODE=DEV` is set

### Issue: Import errors in Python

**Solution:**
- Ensure you're in the project root directory
- Activate your virtual environment if using one
- Reinstall dependencies: `pip install -r requirements.txt`

### Issue: Make command not found (Windows)

**Solution:** 
- Use the PowerShell commands provided in this guide instead
- Or install make via Chocolatey: `choco install make`

## Additional Development Commands

### Available Make Commands (Linux/Mac)

- `make build` - Build and install the Python package
- `make terptracker-dev` - Start development server with local DynamoDB
- `make app-dev` - Alternative development server command
- `make compose-db` - Start only the DynamoDB containers
- `make install_requirements` - Install Python dependencies

### Docker Compose Commands

- `docker compose up -d` - Start containers in detached mode
- `docker compose down` - Stop and remove containers
- `docker compose logs` - View container logs
- `docker compose ps` - List running containers

## Next Steps

After setup:
1. Visit `http://localhost:5000` to access the application
2. Create an account and start tracking expenses
3. See [README.md](README.md) for usage instructions and project overview

