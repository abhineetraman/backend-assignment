#This is a python script for APIs for events

import os
from flask_restful import Resource, Api,  fields, marshal_with, reqparse
from flask import Flask, send_file
import requests
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import distance, geodesic

from applications.validations import BusinessValidationError, NotFoundError


app = Flask(__name__)

api = Api(app)
app.app_context().push()


#EventData Class stores and initializes the data of csv file for manipulation

class EventData():
    def __init__(self):
        event_data = pd.read_csv('static/event_data.csv')
        event_data['date'] = event_data['date'].apply(pd.to_datetime, format='%Y-%m-%d')
        self.event_data = event_data

    def get_event_data(self):
        return self.event_data

def get_weather_forecast(city, date):
    """
    Retrieves weather conditions for an event based on its location and date for the next 14 days.

    Args:
        city: The city where the event is taking place.
        date: The date of the event.

    Returns:
        A dictionary containing the weather forecast for the next 14 days.
    """

    # Replace with your API endpoint and access code
    api_endpoint = "https://gg-backend-assignment.azurewebsites.net/api/Weather"
    api_access_code = "KfQnTWHJbg1giyB_Q9Ih3Xu3L9QOBDTuU5zwqVikZepCAzFut3rqsg=="

    # Construct the API request URL
    url = f"{api_endpoint}?code={api_access_code}&city={city}&date={date}"

    # Send the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the weather forecast data
        return response.json()
    else:
        # Handle the error
        raise Exception(f"API request failed with status code: {response.status_code}")

def calculate_distance(user_latitude, user_longitude, event_latitude, event_longitude):
    """
    Calculates the distance between the user's location and the event location.

    Args:
        user_latitude: The user's latitude.
        user_longitude: The user's longitude.
        event_latitude: The event's latitude.
        event_longitude: The event's longitude.

    Returns:
        The distance between the user's location and the event location in miles.
    """

    # Replace with your API endpoint and access code
    api_endpoint = "https://gg-backend-assignment.azurewebsites.net/api/Distance"
    api_access_code = "IAKvV2EvJa6Z6dEIUqqd7yGAu7IZ8gaH-a0QO6btjRc1AzFu8Y3IcQ=="

    # Construct the API request URL
    url = f"{api_endpoint}?code={api_access_code}&latitude1={user_latitude}&longitude1={user_longitude}&latitude2={event_latitude}&longitude2={event_longitude}"

    # Send the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the distance value
        distance = response.json()['distance']

        # Return the distance in miles
        return distance
    else:
        # Handle the error
        raise Exception(f"API request failedwith status code: {response.status_code}")



#Arguments from frontend for API for add new events

create_event_parser = reqparse.RequestParser()
create_event_parser.add_argument('event_name')
create_event_parser.add_argument('city_name')
create_event_parser.add_argument('date')
create_event_parser.add_argument('time')
create_event_parser.add_argument('latitude')
create_event_parser.add_argument('longitude')


#API for adding new events

class EventAPI(Resource):
    def post(self):
        event_data = EventData().get_event_data()

        args = create_event_parser.parse_args()
        event_name = args.get("event_name", None)
        city_name = args.get("city_name", None)
        date = args.get("date", None)
        time = args.get("time", None)
        latitude = args.get("latitude", None)
        longitude = args.get("longitude", None)
        
        if event_name is None:
            raise BusinessValidationError(status_code=400, error_code="BE1000", error_message="Event Name is Required")
        if city_name is None:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="City Name is Required")
        if date is None:
            raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="Date is Required")
        if time is None:
            raise BusinessValidationError(status_code=400, error_code="BE1003", error_message="Time is Required")
        if latitude is None:
            raise BusinessValidationError(status_code=400, error_code="BE1004", error_message="Latitude is Required")
        if longitude is None:
            raise BusinessValidationError(status_code=400, error_code="BE1005", error_message="Longitude is Required")
        new_row = {'event_name': event_name, 'city_name': city_name, 'date': date, 'time': time, 'latitude': latitude, 'longitude': longitude}

        event_data = pd.concat([event_data, pd.DataFrame([new_row])], ignore_index=True)
        
        return "Event is Added Successfully", 200

#Arguments from frontend for API for get events and output data format

find_event_parser = reqparse.RequestParser()
find_event_parser.add_argument('user_latitude')
find_event_parser.add_argument('user_longitude')
find_event_parser.add_argument('date')

show_output = {
    "event_name": fields.String,
    "city": fields.String,
    "date": fields.String,
    "weather": fields.String,
    "distance": fields.Float
}

#API find finding events

class EventFindAPI(Resource):
    @marshal_with(show_output)
    def post(self):

        args = find_event_parser.parse_args()
        user_latitude = args.get("user_latitude", None)
        user_longitude = args.get("user_longitude", None)
        date = args.get("date", None)

        if user_latitude is None:
            raise BusinessValidationError(status_code=400, error_code="BE2000", error_message="User Latitude is Required")
        if user_longitude is None:
            raise BusinessValidationError(status_code=400, error_code="BE2001", error_message="User Longitude is Required")
        if date is None:
            raise BusinessValidationError(status_code=400, error_code="BE2002", error_message="Date is Required")
        
        date = pd.Timestamp(date)
        event_data = EventData().get_event_data()
        filtered_data = event_data[(event_data['date'] >= date) & (event_data['date'] <= date + pd.Timedelta(days=14))]
        sorted_data = filtered_data.sort_values(by=['date', 'time'], ascending=False)
        sorted_data = sorted_data.reset_index(drop=True)

        if len(sorted_data) == 0:
            raise NotFoundError(status_code=404)

        output_df = pd.DataFrame()
        output_df['event_name'] = sorted_data['event_name']
        output_df['city'] = sorted_data['city_name']
        output_df['date'] = sorted_data['date'].astype(str)
       
        #added temp_df to store weather and distance data for each event temprorarily
        weather_df = pd.DataFrame()
        distance_df = pd.DataFrame(columns=['distance_km'])

        for _, row in sorted_data.iterrows():
            city = row['city_name']
            date = row['date']
            latitude = row['latitude']
            longitude = row['longitude']

            point1 = ( latitude, longitude)
            point2 = (user_latitude, user_longitude)
            distance_km = geodesic(point1, point2).km
            distance_df = pd.concat([distance_df, pd.DataFrame({'distance_km': [distance_km]})], ignore_index=True)
            

            weather_forecast = get_weather_forecast(city, date)
            weather_df = pd.concat([weather_df, pd.DataFrame([weather_forecast])], ignore_index=True)

        output_df['weather'] = weather_df['weather']
        output_df['distance_km'] = distance_df['distance_km']

        return output_df.to_json(), 200

api.add_resource(EventAPI, '/event')
api.add_resource(EventFindAPI, '/events/find')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
