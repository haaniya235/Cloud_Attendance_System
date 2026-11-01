import firebase_admin
from firebase_admin import credentials, firestore
import os

# Get the current project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Locate Firebase service account key
KEY_PATH = os.path.join(BASE_DIR, "firebase_key.json")

# Initialize Firebase connection
if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)

# Connect to Cloud Firestore
db = firestore.client()

print("Firebase connected successfully!")