# Configuration settings for the Masaraq project

import os

class Config:
    # General settings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Data directories
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    UPLOADS_DIR = os.path.join(DATA_DIR, 'uploads')
    MODELS_DIR = os.path.join(DATA_DIR, 'models')
    GENERATED_DIR = os.path.join(DATA_DIR, 'generated')
    RAW_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
    
    # Machine Learning settings
    MODEL_NAME = 'recommendation_model'
    INTEREST_ASSESSMENT_THRESHOLD = 0.5
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    
    # Other configurations can be added here as needed