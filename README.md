# AirlineManagementSystem

## Overview
This project is a web API developed using Django REST Framework (DRF) to facilitate flight and reservation management for an airline company. The system enables managing flights, airplanes, and reservations efficiently.

## Features
### Airplane Management
- Add, update, and delete airplanes.
- Store airplane details such as tail number, model, capacity, and production year.

### Flight Management
- Add, update, and delete flights.
- Store flight details such as flight number, departure and destination locations, departure and arrival times.
- Validations to prevent the same airplane from being used in multiple flights during the same time frame.

### Reservation Management
- Allow passengers to make reservations for flights.
- Automatically generate reservation codes.
- Manage reservation status (active/inactive).

## Technologies Used
### Backend
- Django
- Django REST Framework (DRF)
- SQLite (for development environment)

## Installation Guide
Follow the steps below to run the project on your local machine.

### 1. Requirements
- Python 3.8 or higher
- Pip (Python package manager)

### 2. Clone the Project
```bash
git clone https://github.com/uzankubra/AirlineManagementSystem.git
cd AirlineManagementSystem
```

### 3. Create and Activate a Virtual Environment
#### Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
### 4. Prepare the Database
```bash
python manage.py migrate
```

### 5. Start the Server
```bash
python manage.py runserver
```
The server will run at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## API Endpoints
### Airplanes
- `GET /api/airplanes/` - List all airplanes.
- `POST /api/airplanes/` - Add a new airplane.
- `GET /api/airplanes/{id}/` - Retrieve details of a specific airplane.
- `PUT /api/airplanes/{id}/` - Update a specific airplane.
- `DELETE /api/airplanes/{id}/` - Delete a specific airplane.

### Flights
- `GET /api/flights/` - List all flights.
- `POST /api/flights/` - Add a new flight.
- `GET /api/flights/{id}/` - Retrieve details of a specific flight.
- `PUT /api/flights/{id}/` - Update a specific flight.
- `DELETE /api/flights/{id}/` - Delete a specific flight.

### Reservations
- `GET /api/reservations/` - List all reservations.
- `POST /api/reservations/` - Add a new reservation.
- `GET /api/reservations/{id}/` - Retrieve details of a specific reservation.
- `PUT /api/reservations/{id}/` - Update a specific reservation.
- `DELETE /api/reservations/{id}/` - Delete a specific reservation.

