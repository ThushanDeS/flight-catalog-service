# Flight Catalog Service ✈️

## Student A - Flight Catalog Microservice

This microservice is part of a Flight Management System. It manages flight information, schedules, and seat availability.

## 📋 Overview

The Flight Catalog Service provides REST APIs for:
- Retrieving flight information
- Searching flights by origin, destination, and date
- Managing seat availability
- Creating new flights (admin)

## 🏗️ Architecture

- **Framework**: Flask (Python)
- **Database**: MongoDB
- **Container**: Docker
- **CI/CD**: GitHub Actions
- **Cloud**: Azure Container Apps

## 🔗 Integration Points

This service is called by:
- **Booking Service**: To check flight availability and get flight details
- **Payment Service**: To get flight pricing information

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Docker
- MongoDB (local or Atlas)
- Azure account (for deployment)

### Local Development

1. Clone the repository
```bash
git clone https://github.com/yourusername/flight-catalog-service.git
cd flight-catalog-service