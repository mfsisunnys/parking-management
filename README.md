#Parking Management

## Description

This is a parking management system that allows park/unpark cars. The system also allows users to view the status of the parking lot and the parking spots.

## Installation

1. Clone the repository
2. Create a virtual environment using the command "python3 -m venv venv"
3. Activate the virtual environment using the command "source venv/bin/activate"
4. Install the requirements using the command "pip install -r requirements.txt"
5. Start the redis server using the command "sudo systemctl start redis-server"
6. Update .env file with the required values
7. Run the command "python manage.py runserver" to start the server

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
2. /auth/register/ - POST - Register
3. /api/v1/parking-lot/ - POST - Create a parking lot
4. /api/v1/vehicle/park/ - POST - Park a car with given vehicle number
5. /api/v1/vehicle/unpark/ - PUT - Unpark a car with given vehicle number
6. api/v1/park/slot/?slot_id - GET - Get the details of a parking slot

## API Usage

1. Register a user using the endpoint /auth/register/
2. Login using the endpoint /auth/login/ and store the authorization token
3. Use the authorization token to access the other endpoints
4. Create a new parking lot using the endpoint /api/v1/parking-lot/
5. Park a car using the endpoint /api/v1/vehicle/park/
6. Unpark a car using the endpoint /api/v1/vehicle/unpark/
7. Get the details of a parking slot using the endpoint /api/v1/park/slot/?slot_id

## Unit Tests

The unit tests can be run using the command "python manage.py test"
