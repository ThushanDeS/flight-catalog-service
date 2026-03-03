"""API routes for flight catalog"""
from flask import Blueprint, request, jsonify

# Create blueprint first
flights_bp = Blueprint('flights', __name__, url_prefix='/api/flights')

# Sample flight data
SAMPLE_FLIGHTS = [
    {
        "id": "FL001",
        "flightNumber": "AA789",
        "airline": "American Airlines",
        "departure": "JFK",
        "arrival": "LAX",
        "departure_time": "2026-04-15T10:30:00Z",
        "arrival_time": "2026-04-15T13:45:00Z",
        "available_seats": 42,
        "price": 299.99
    },
    {
        "id": "FL002",
        "flightNumber": "UA456",
        "airline": "United Airlines",
        "departure": "SFO",
        "arrival": "ORD",
        "departure_time": "2026-04-15T14:20:00Z",
        "arrival_time": "2026-04-15T17:30:00Z",
        "available_seats": 38,
        "price": 199.99
    },
    {
        "id": "FL003",
        "flightNumber": "DL123",
        "airline": "Delta Airlines",
        "departure": "ATL",
        "arrival": "MIA",
        "departure_time": "2026-04-16T08:15:00Z",
        "arrival_time": "2026-04-16T09:45:00Z",
        "available_seats": 55,
        "price": 149.99
    },
    {
        "id": "FL004",
        "flightNumber": "SW234",
        "airline": "Southwest Airlines",
        "departure": "DEN",
        "arrival": "LAS",
        "departure_time": "2026-04-16T11:30:00Z",
        "arrival_time": "2026-04-16T12:45:00Z",
        "available_seats": 28,
        "price": 89.99
    }
]


@flights_bp.route('/', methods=['GET'])
def get_flights():
    """Get all flights"""
    return jsonify({
        'status': 'success',
        'message': 'Flights retrieved successfully',
        'data': SAMPLE_FLIGHTS
    }), 200


@flights_bp.route('/<flight_id>', methods=['GET'])
def get_flight(flight_id):
    """Get a specific flight"""
    # Find flight by ID
    flight = next((f for f in SAMPLE_FLIGHTS if f['id'] == flight_id), None)
    
    if flight:
        return jsonify({
            'status': 'success',
            'message': f'Flight {flight_id} retrieved',
            'data': flight
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': f'Flight {flight_id} not found',
            'data': None
        }), 404


@flights_bp.route('/', methods=['POST'])
def create_flight():
    """Create a new flight"""
    data = request.get_json()
    
    # Generate a new ID
    new_id = f"FL{len(SAMPLE_FLIGHTS) + 1:03d}"
    data['id'] = new_id
    
    # In a real app, you'd save to database
    # Here we just return the created flight
    
    return jsonify({
        'status': 'success',
        'message': 'Flight created successfully',
        'data': data
    }), 201


@flights_bp.route('/search', methods=['GET'])
def search_flights():
    """Search flights by departure and arrival"""
    departure = request.args.get('departure', '').upper()
    arrival = request.args.get('arrival', '').upper()
    date = request.args.get('date')
    
    # Filter flights
    results = SAMPLE_FLIGHTS.copy()
    
    if departure:
        results = [f for f in results if f['departure'] == departure]
    
    if arrival:
        results = [f for f in results if f['arrival'] == arrival]
    
    if date:
        results = [f for f in results if date in f['departure_time']]
    
    return jsonify({
        'status': 'success',
        'message': 'Search results',
        'data': results,
        'filters': {
            'departure': departure,
            'arrival': arrival,
            'date': date
        }
    }), 200


@flights_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'service': 'flight-catalog',
        'status': 'healthy',
        'database': 'connected (sample data)',
        'flights_count': len(SAMPLE_FLIGHTS)
    }), 200