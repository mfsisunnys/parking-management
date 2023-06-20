#Parking Management

## Description

This is a parking management system that allows park/unpark cars. The system also allows users to view the status of the parking lot and the parking spots.

## Installation

1. Clone the repository
2. Create a virtual environment using the command "python3 -m venv venv"
3. Activate the virtual environment using the command "source venv/bin/activate"
4. Install the requirements using the command "pip install -r requirements.txt"
5. Run the command "python manage.py runserver" to start the server

## Tools Used

1. Python
2. Django
3. Django Rest Framework
4. SQLite
5. Swagger

## API Documentation

The API documentation can be found at http://localhost:8000/docs/

## API Endpoints

1. /auth/login/ - POST - Login
2. /api/park/ - POST - Park a car
3. /api/unpark/{vehicle_number} - POST - Unpark a car
4. /slots/slot/id/ - GET - Get the details of a parking spot

## Unit Tests

The unit tests can be run using the command "python manage.py test"
