import sys
sys.path.append('../..')
from main import EventAPI, EventFindAPI
import pytest
import requests


def test_add_events():
    test_data = {
        "event_name" : "Test_event",
        "city_name" : "Patna",
        "date" : "2022-01-01",
        "time" : "15:00:00",
        "latitude" : 105.234567567444,
        "longitude" : 105.234567567444,
    }

    response = requests.post('http://localhost:5000/event', json=test_data)
    assert response.status_code == 200
    assert response.json() == 'Event is Added Successfully'

def test_add_events_missing_event_name():
    test_data = {
        "event_name" : None,
        "city_name" : "Patna",
        "date" : "2022-01-01",
        "time" : "15:00:00",
        "latitude" : 105.234567567444,
        "longitude" : 105.234567567444,
    }

    response = requests.post('http://localhost:5000/event', json=test_data)
    assert response.status_code == 400
    assert response.json() == {'error_code': 'BE1000', 'error_message': 'Event Name is Required'}

def test_add_events_missing_city_name():
    test_data = {
        "event_name" : 'Test',
        "city_name" : None,
        "date" : "2022-01-01",
        "time" : "15:00:00",
        "latitude" : 105.234567567444,
        "longitude" : 105.234567567444,
    }

    response = requests.post('http://localhost:5000/event', json=test_data)
    assert response.status_code == 400
    assert response.json() == {'error_code': 'BE1001', 'error_message': 'City Name is Required'}

def test_add_events_missing_date():
    test_data = {
        "event_name" : 'Test',
        "city_name" : "Patna",
        "date" : None,
        "time" : "15:00:00",
        "latitude" : 105.234567567444,
        "longitude" : 105.234567567444,
    }

    response = requests.post('http://localhost:5000/event', json=test_data)
    assert response.status_code == 400
    assert response.json() == {'error_code': 'BE1002', 'error_message': 'Date is Required'}

def test_add_events_missing_time():
    test_data = {
        "event_name" : 'Test',
        "city_name" : "Patna",
        "date" : "2022-01-01",
        "time" : None,
        "latitude" : 105.234567567444,
        "longitude" : 105.234567567444,
    }

    response = requests.post('http://localhost:5000/event', json=test_data)
    assert response.status_code == 400
    assert response.json() == {'error_code': 'BE1003', 'error_message': 'Time is Required'}

def test_add_events_missing_latitude():
    test_data = {
        "event_name" : 'Test',
        "city_name" : "Patna",
        "date" : "2022-01-01",
        "time" : "15:00:00",
        "latitude" : None,
        "longitude" : 105.234567567444,
    }

    response = requests.post('http://localhost:5000/event', json=test_data)
    assert response.status_code == 400
    assert response.json() == {'error_code': 'BE1004', 'error_message': 'Latitude is Required'}

def test_add_events_missing_longitude():
    test_data = {
        "event_name" : 'Test',
        "city_name" : "Patna",
        "date" : "2022-01-01",
        "time" : "15:00:00",
        "latitude" : 105.234567567444,
        "longitude" : None,
    }

    response = requests.post('http://localhost:5000/event', json=test_data)
    assert response.status_code == 400
    assert response.json() == {'error_code': 'BE1005', 'error_message': 'Longitude is Required'}

def test_event_find_null():
    test_data = {
        "date" : "2023-03-01",
        "user_latitude" : 105.234567567444,
        "user_longitude" : 102.23564777381,
    }

    response = requests.post('http://localhost:5000/events/find', json=test_data)
    assert response.status_code == 404
    #assert response.json() == 'Events not Found'

def test_event_find_missing_date():
    test_data = {
        "date" : None,
        "user_latitude" : 105.234567567444,
        "user_longitude" : 102.23564777381,
    }

    response = requests.post('http://localhost:5000/events/find', json=test_data)
    assert response.status_code == 400
    assert response.json() == {'error_code' : "BE2002", 'error_message': "Date is Required"}

def test_event_find_missing_latitude():
    test_data = {
        "date" : "2024-03-01",
        "user_latitude" : None,
        "user_longitude" : 102.23564777381,
    }

    response = requests.post('http://localhost:5000/events/find', json=test_data)
    assert response.status_code == 400
    assert response.json() == {'error_code' : "BE2000", 'error_message': "User Latitude is Required"}

def test_event_find_missing_date():
    test_data = {
        "date" : "2024-03-01",
        "user_latitude" : 105.234567567444,
        "user_longitude" : None,
    }

    response = requests.post('http://localhost:5000/events/find', json=test_data)
    assert response.status_code == 400
    assert response.json() == {'error_code' : "BE2001", 'error_message': "User Longitude is Required"}

def test_event_find():
    test_data = {
        "date" : "2024-03-01",
        "user_latitude" : 85.234567567444,
        "user_longitude" : 82.23564777381,
    }

    response = requests.post('http://localhost:5000/events/find', json=test_data)
    assert response.status_code == 200
    #assert response.json() == {'event_name': None, 'city': None, 'date': None, 'weather': None, 'distance': None}