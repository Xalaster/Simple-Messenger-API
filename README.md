# Simple-Messenger-API

This simple messenger API project creates a SQLite database and leverages FastAPI to facilitate endpoints to create and fetch messages from the database.

## Initial Setup
1. Make use of the requirements.txt file to ensure all necessary packages are installed. 
2. Run the Python setup script to create the messenger_db.db SQLite file and create 500 sample users and 1500 sample messages.
   > python db_setup_and_test.py

## Launch API
1. Run the live server by launching using uvicorn.
   > uvicorn main:app --reload
2. Visit http://127.0.0.1:8000/docs to view the Swagger page and view API documentation.

## Test API
Pytest tests exist in the test_main.py file. Invoking pytest in the project directory will automatically detect the tests, execute them, and report the results.
