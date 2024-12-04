import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('')

# Database Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'reva_db')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'user_data')

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'your-username'),
    'password': os.getenv('MYSQL_PASSWORD', 'your-password'),
    'database': os.getenv('MYSQL_DATABASE', 'reva_db')
}

# SQLite Configuration
SQLITE_DB_PATH = 'reva.db'

# Voice Configuration
VOICE_TYPE = 'female'
VOICE_RATE = 175
VOICE_VOLUME = 1.0

# Security Configuration
ANTIVIRUS_PATH = "C:/Program Files/McAfee/MSC/mcconsol.exe"
