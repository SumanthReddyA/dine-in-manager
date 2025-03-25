# backend/tests/conftest.py
import sys
import os
os.environ['TESTING_ENV'] = 'TRUE'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.src.app import app
print(sys.path)
print("TESTING MODE:", app.config['TESTING'])
print("TESTING_ENV from conftest:", os.environ.get('TESTING_ENV')) # Print TESTING_ENV
print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])
