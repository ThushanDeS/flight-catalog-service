"""Database models for flight catalog"""
from datetime import datetime


class Flight:
    """Flight model"""
    
    def __init__(self, flight_id, airline, departure, arrival, departure_time, arrival_time, price):
        self.flight_id = flight_id
        self.airline = airline
        self.departure = departure
        self.arrival = arrival
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert flight to dictionary"""
        return {
            'flight_id': self.flight_id,
            'airline': self.airline,
            'departure': self.departure,
            'arrival': self.arrival,
            'departure_time': self.departure_time,
            'arrival_time': self.arrival_time,
            'price': self.price,
            'created_at': self.created_at.isoformat()
        }


class Airport:
    """Airport model"""
    
    def __init__(self, code, name, city, country):
        self.code = code
        self.name = name
        self.city = city
        self.country = country
    
    def to_dict(self):
        """Convert airport to dictionary"""
        return {
            'code': self.code,
            'name': self.name,
            'city': self.city,
            'country': self.country
        }
