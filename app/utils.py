"""Utility functions"""


def serialize_flight(flight):
    """Serialize flight object"""
    return flight.to_dict() if hasattr(flight, 'to_dict') else flight


def parse_date(date_string):
    """Parse date string"""
    from datetime import datetime
    try:
        return datetime.fromisoformat(date_string)
    except ValueError:
        return None


def calculate_duration(departure_time, arrival_time):
    """Calculate flight duration"""
    from datetime import datetime
    if isinstance(departure_time, str):
        departure_time = datetime.fromisoformat(departure_time)
    if isinstance(arrival_time, str):
        arrival_time = datetime.fromisoformat(arrival_time)
    
    return arrival_time - departure_time
