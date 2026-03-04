"""Database models for flight catalog"""
from datetime import datetime
import os
import logging
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ===== MongoDB Connection Class =====

class MongoDBConnection:
    """Handles MongoDB connection and operations"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.flights_collection = None
        self.airports_collection = None
        self.connected = False
        self.connect()
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            # Get connection string from environment
            mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
            mongo_db = os.getenv('MONGO_DB', 'flight_db')
            
            # Connect to MongoDB
            self.client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[mongo_db]
            self.flights_collection = self.db.flights
            self.airports_collection = self.db.airports
            
            # Create indexes
            self._create_indexes()
            
            self.connected = True
            logger.info(f"✅ Connected to MongoDB: {mongo_db}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            self.connected = False
            logger.error(f"❌ MongoDB connection error: {e}")
        except Exception as e:
            self.connected = False
            logger.error(f"❌ Unexpected error: {e}")
    
    def _create_indexes(self):
        """Create database indexes"""
        if self.flights_collection is not None:
            try:
                # Unique index on flight number
                self.flights_collection.create_index([("flightNumber", ASCENDING)], unique=True)
                # Index for searches
                self.flights_collection.create_index([
                    ("departure", ASCENDING),
                    ("arrival", ASCENDING),
                    ("departure_date", ASCENDING)
                ])
                logger.info("✅ Database indexes created")
            except Exception as e:
                logger.warning(f"⚠️ Index creation failed: {e}")
    
    def get_status(self):
        """Get database connection status"""
        status = {
            "connected": self.connected,
            "collections": {
                "flights": 0,
                "airports": 0
            }
        }
        
        if self.connected and self.flights_collection is not None:
            try:
                status["collections"]["flights"] = self.flights_collection.count_documents({})
                if self.airports_collection is not None:
                    status["collections"]["airports"] = self.airports_collection.count_documents({})
            except Exception as e:
                logger.error(f"Error getting collection counts: {e}")
        
        return status


# Create global database connection instance
db = MongoDBConnection()


# ===== Model Classes =====

class Flight:
    """Flight model"""
    
    def __init__(self, flight_id, airline, departure, arrival, departure_time, arrival_time, price, available_seats=100):
        self.flight_id = flight_id
        self.airline = airline
        self.departure = departure
        self.arrival = arrival
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price
        self.available_seats = available_seats
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert flight to dictionary"""
        return {
            'flight_id': self.flight_id,
            'airline': self.airline,
            'departure': self.departure,
            'arrival': self.arrival,
            'departure_time': self.departure_time.isoformat() if isinstance(self.departure_time, datetime) else self.departure_time,
            'arrival_time': self.arrival_time.isoformat() if isinstance(self.arrival_time, datetime) else self.arrival_time,
            'price': self.price,
            'available_seats': self.available_seats,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        """Create Flight instance from dictionary"""
        return Flight(
            flight_id=data.get('flight_id'),
            airline=data.get('airline'),
            departure=data.get('departure'),
            arrival=data.get('arrival'),
            departure_time=data.get('departure_time'),
            arrival_time=data.get('arrival_time'),
            price=data.get('price'),
            available_seats=data.get('available_seats', 100)
        )
    
    def save_to_db(self):
        """Save this flight to MongoDB"""
        if db.connected and db.flights_collection is not None:
            flight_dict = self.to_dict()
            # Remove _id if present to avoid conflicts
            flight_dict.pop('_id', None)
            result = db.flights_collection.insert_one(flight_dict)
            return str(result.inserted_id)
        return None
    
    @staticmethod
    def find_by_id(flight_id):
        """Find flight by ID in MongoDB"""
        if db.connected and db.flights_collection is not None:
            try:
                if ObjectId.is_valid(flight_id):
                    data = db.flights_collection.find_one({"_id": ObjectId(flight_id)})
                    if data:
                        data['_id'] = str(data['_id'])
                        return data
            except Exception as e:
                logger.error(f"Error finding flight by ID: {e}")
        return None
    
    @staticmethod
    def find_all():
        """Get all flights from MongoDB"""
        if db.connected and db.flights_collection is not None:
            try:
                flights = list(db.flights_collection.find())
                for flight in flights:
                    flight['_id'] = str(flight['_id'])
                return flights
            except Exception as e:
                logger.error(f"Error finding all flights: {e}")
        return []


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
    
    @staticmethod
    def find_by_code(code):
        """Find airport by code"""
        if db.connected and db.airports_collection is not None:
            try:
                data = db.airports_collection.find_one({"code": code.upper()})
                if data:
                    data['_id'] = str(data['_id'])
                    return data
            except Exception as e:
                logger.error(f"Error finding airport by code: {e}")
        return None


# ===== Functions for app.py to import =====

def init_db():
    """Initialize database with sample data if empty"""
    logger.info("📦 Initializing database...")
    
    if not db.connected:
        logger.warning("⚠️ Database not connected, skipping initialization")
        return False
    
    # Initialize airports if empty
    if db.airports_collection is not None and db.airports_collection.count_documents({}) == 0:
        logger.info("📦 Adding sample airports...")
        sample_airports = [
            {"code": "JFK", "name": "John F Kennedy International", "city": "New York", "country": "USA"},
            {"code": "LAX", "name": "Los Angeles International", "city": "Los Angeles", "country": "USA"},
            {"code": "ORD", "name": "O'Hare International", "city": "Chicago", "country": "USA"},
            {"code": "ATL", "name": "Hartsfield-Jackson Atlanta International", "city": "Atlanta", "country": "USA"},
            {"code": "DFW", "name": "Dallas/Fort Worth International", "city": "Dallas", "country": "USA"},
            {"code": "DEN", "name": "Denver International", "city": "Denver", "country": "USA"}
        ]
        try:
            db.airports_collection.insert_many(sample_airports)
            logger.info(f"✅ Added {len(sample_airports)} sample airports")
        except Exception as e:
            logger.error(f"❌ Failed to add sample airports: {e}")
    
    # Initialize flights if empty
    if db.flights_collection is not None and db.flights_collection.count_documents({}) == 0:
        logger.info("📦 Adding sample flights...")
        sample_flights = [
            {
                "flightNumber": "AA789",
                "airline": "American Airlines",
                "departure": "JFK",
                "arrival": "LAX",
                "departure_time": "2026-04-15T10:30:00Z",
                "arrival_time": "2026-04-15T13:45:00Z",
                "available_seats": 42,
                "price": 299.99,
                "departure_date": "2026-04-15"
            },
            {
                "flightNumber": "UA456",
                "airline": "United Airlines",
                "departure": "SFO",
                "arrival": "ORD",
                "departure_time": "2026-04-15T14:20:00Z",
                "arrival_time": "2026-04-15T17:30:00Z",
                "available_seats": 38,
                "price": 199.99,
                "departure_date": "2026-04-15"
            },
            {
                "flightNumber": "DL123",
                "airline": "Delta Airlines",
                "departure": "ATL",
                "arrival": "MIA",
                "departure_time": "2026-04-16T08:15:00Z",
                "arrival_time": "2026-04-16T09:45:00Z",
                "available_seats": 55,
                "price": 149.99,
                "departure_date": "2026-04-16"
            }
        ]
        try:
            db.flights_collection.insert_many(sample_flights)
            logger.info(f"✅ Added {len(sample_flights)} sample flights")
        except Exception as e:
            logger.error(f"❌ Failed to add sample flights: {e}")
    
    return True


def get_db_status():
    """Get database connection status for health checks"""
    return db.get_status()