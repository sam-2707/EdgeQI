"""
Configuration settings for EDGE-QI Backend
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "EDGE-QI API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Backend for EDGE-QI Smart City Platform"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/edge_qi"
    DB_ECHO: bool = False
    
    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # MQTT Settings
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # WebSocket Settings
    WS_PING_INTERVAL: int = 25
    WS_PING_TIMEOUT: int = 20
    
    # Metrics Broadcasting
    METRICS_BROADCAST_INTERVAL: int = 5  # seconds
    
    # Data Retention
    MAX_DETECTIONS_IN_MEMORY: int = 1000
    MAX_LOGS_IN_MEMORY: int = 500
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
