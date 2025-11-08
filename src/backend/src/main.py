"""
EDGE-QI Backend API Server
FastAPI application with WebSocket support
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import socketio
import asyncio
from contextlib import asynccontextmanager

from .config import settings
# from .database import init_db, close_db, get_db
from .services.websocket_service import ws_service
from .routers import system, nodes
from .routers.mock_routers import detection_router, analytics_router, logs_router, consensus_router


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events: startup and shutdown
    """
    # Startup
    print("🚀 Starting EDGE-QI Backend Server...")
    # await init_db()  # Skip database for now
    
    # Start metrics broadcaster in background (skip for now)
    # asyncio.create_task(ws_service.start_metrics_broadcaster(get_db))
    
    print("✅ Server started successfully (without database)")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down EDGE-QI Backend Server...")
    # await close_db()
    print("✅ Server shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Create Socket.IO ASGI app
socket_app = socketio.ASGIApp(
    ws_service.sio,
    app,
    socketio_path='/socket.io'
)

# Register API routers
app.include_router(system.router, prefix="/api/system", tags=["System"])
app.include_router(nodes.router, prefix="/api/nodes", tags=["Edge Nodes"])
app.include_router(detection_router, prefix="/api/detections", tags=["Detection"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(logs_router, prefix="/api/logs", tags=["Logs"])
app.include_router(consensus_router, prefix="/api/consensus", tags=["Consensus"])


# Root endpoint
@app.get("/")
async def root():
    """
    API root endpoint
    """
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "docs": "/docs",
        "websocket": "/socket.io"
    }


# Health check endpoint
@app.get("/health")
async def health():
    """
    Simple health check
    """
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:socket_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
