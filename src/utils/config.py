"""
Configuration utilities for the hotel management toolbox.
Centralizes environment variable handling and configuration management.
"""

import os
from typing import Optional


class Config:
    """Centralized configuration management for the hotel toolbox."""
    
    # Database configuration
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'toolbox_db')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'toolboxuser')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    
    # Toolbox server configuration
    TOOLBOX_HOST = os.getenv('TOOLBOX_HOST', '127.0.0.1')
    TOOLBOX_PORT = os.getenv('TOOLBOX_PORT', '5001')
    
    # Google AI configuration
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the PostgreSQL connection URL."""
        return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DATABASE}"
    
    @classmethod
    def get_toolbox_url(cls) -> str:
        """Get the toolbox server URL."""
        return f"http://{cls.TOOLBOX_HOST}:{cls.TOOLBOX_PORT}"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present."""
        required_vars = [
            'POSTGRES_PASSWORD',
            'GOOGLE_API_KEY'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False
        
        return True 