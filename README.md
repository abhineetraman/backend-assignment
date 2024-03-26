# Flask Event API Project


## Project Overview
This project is an API for managing events. It allows users to add new events and find events based on their location and date.


## Tech Stack and Databases

The project uses the following tech stack:

* Python: A versatile programming language that is widely used for web development.
* Flask: A lightweight web framework for building web applications.
* Pandas: A powerful data analysis library for Python.
* NumPy: A library for scientific computing with Python.
* GeoPy: A library for geocoding and distance calculations.

### Databases has not implemented yet but can be modified to any SQL databases like MySQL, Postgres, SQLite, etc.


## Design Decisions
The following design decisions were made:

* The API uses a RESTful architecture, which makes it easy to use and integrate with other applications.
* The API uses JSON as the data format, which is a lightweight and easy-to-parse format.
* The API uses Flask-RESTful, a library that simplifies the development of RESTful APIs in Flask.
* The API uses Pandas to read and manipulate the event data.
* The API uses NumPy to perform distance calculations.
* The API uses GeoPy to geocode locations and calculate distances.

## Challenges and solutions
The following challenges were encountered and addressed:


**Calculating distances**: The distance between the user's location and the event location was calculated using Geopy instead of link for quick implementation.

**Retrieving weather data**: The weather forecast for each event was retrieved from an external API.
To set up and run the project, follow these steps:

## Setup and Run Instructions

Clone the project repository.

Setup the virtual environment

* python3 -m venv venv

Activate the Virtual Environment

* source venv/bin/activate
  
Install the required Python packages.

* pip install -r requirements.txt

Run the Flask app.
Run the following command to start the Flask development server:
python3 app.py


The API will be available at http://localhost:5000.

The API has the following endpoints:

/event: Adds a new event.
/events/find: Finds events based on the user's location and date.
