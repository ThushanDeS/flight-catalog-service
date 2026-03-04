"""Tests for flight endpoints"""
import unittest
from app import create_app


class FlightTestCase(unittest.TestCase):
    """Test cases for flight API"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_get_flights(self):
        """Test getting all flights"""
        response = self.client.get('/api/flights/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
    
    def test_get_flight_by_id(self):
        """Test getting a specific flight"""
        response = self.client.get('/api/flights/flight123')
        self.assertEqual(response.status_code, 200)
    
    def test_create_flight(self):
        """Test creating a new flight"""
        flight_data = {
            'airline': 'Test Airlines',
            'departure': 'LAX',
            'arrival': 'JFK',
            'departure_time': '2026-03-10T10:00:00',
            'arrival_time': '2026-03-10T18:00:00',
            'price': 500
        }
        response = self.client.post('/api/flights/', json=flight_data)
        self.assertEqual(response.status_code, 201)
    
    def test_search_flights(self):
        """Test searching flights"""
        response = self.client.get('/api/flights/search?departure=LAX&arrival=JFK&date=2026-03-10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')


if __name__ == '__main__':
    unittest.main()
