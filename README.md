# NAOMI API

[![codecov](https://codecov.io/gh/reubenjohn/naomi_api/branch/main/graph/badge.svg?token=naomi_api_token_here)](https://codecov.io/gh/reubenjohn/naomi_api/branch/main)
[![CI](https://github.com/reubenjohn/naomi_api/actions/workflows/main.yml/badge.svg)](https://github.com/reubenjohn/naomi_api/actions/workflows/main.yml)

A FastAPI service for handling webhooks and push notifications integrated with the NAOMI core library.

## Overview

NAOMI API provides:

* Webhook event processing and storage
* Firebase Cloud Messaging (FCM) integration for push notifications 
* RESTful API endpoints built with FastAPI
* Integration with the NAOMI core library

## Installation

```bash
# Clone the repository
git clone https://github.com/reubenjohn/naomi_api.git
cd naomi_api

# Install dependencies
make install
```

## Configuration

Copy `.env.example` to `.env` and fill in your environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration values
```

Required environment variables include:

### Firebase Configuration

```
# Firebase Web Configuration
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project_id.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
FIREBASE_APP_ID=your_app_id
FIREBASE_MEASUREMENT_ID=your_measurement_id
FIREBASE_VAPID_KEY=your_vapid_key

# Firebase Admin SDK Configuration
FIREBASE_ADMIN_TYPE=service_account
FIREBASE_ADMIN_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_ADMIN_PRIVATE_KEY=your_private_key  # Include newlines with \n
FIREBASE_ADMIN_CLIENT_EMAIL=your_client_email
FIREBASE_ADMIN_CLIENT_ID=your_client_id
FIREBASE_ADMIN_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_ADMIN_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_ADMIN_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_ADMIN_CLIENT_CERT_URL=your_client_cert_url
FIREBASE_ADMIN_UNIVERSE_DOMAIN=googleapis.com
```

### NAOMI Core Configuration

```
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_MODEL=gpt-4
```

### Frontend Integration

```
STREAMLIT_URL=http://localhost:8501  # URL of your Streamlit frontend
```

## Running the Service

```bash
# Start the API server (default: 0.0.0.0:8090)
poetry run api_server

# With custom host/port
poetry run api_server --host 127.0.0.1 --port 8000
```

## API Endpoints

* `POST /webhook` - Receive webhook events
* `POST /notifications/subscribe` - Subscribe a device to notifications (FCM)
* `POST /notifications/send` - Send notifications to subscribed devices

## Development

```bash
# Format code
make fmt

# Lint code
make lint

# Run tests
make test

# Run specific test
poetry run pytest tests/test_api.py::test_receive_webhook -v

# Watch tests (rerun on file changes)
make watch
```

## Project Structure

```
naomi_api/
├── api.py         # FastAPI app and endpoints
├── __init__.py    # Package initialization
├── __main__.py    # CLI entry point
└── sanity.py      # Health check utilities

tests/
├── conftest.py    # Test fixtures and configuration
├── data.py        # Test data objects
└── test_api.py    # API endpoint tests
```

## Dependencies

* FastAPI - Web framework
* Uvicorn - ASGI server
* Firebase Admin - Push notifications
* NAOMI Core - Core functionality (imported from GitHub)
* SQLAlchemy - Database ORM