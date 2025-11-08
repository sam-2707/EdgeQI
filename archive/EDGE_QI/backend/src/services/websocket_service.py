"""
WebSocket service for real-time updates
"""
import socketio
import asyncio
from datetime import datetime
from typing import Dict, Any, List
from collections import deque


class WebSocketService:
    def __init__(self):
        self.sio = socketio.AsyncServer(
            async_mode='asgi',
            cors_allowed_origins='*',
            logger=True,
            engineio_logger=False
        )
        
        # In-memory storage for recent data
        self.recent_detections: deque = deque(maxlen=1000)
        self.recent_logs: deque = deque(maxlen=500)
        self.active_alerts: List[Dict] = []
        
        # Setup event handlers
        self._setup_events()
    
    def _setup_events(self):
        """Setup Socket.IO event handlers"""
        
        @self.sio.event
        async def connect(sid, environ):
            print(f"✅ Client connected: {sid}")
            await self.sio.emit('connection_established', {
                'status': 'connected',
                'timestamp': datetime.utcnow().isoformat()
            }, room=sid)
            
            # Send initial data
            await self._send_initial_data(sid)
        
        @self.sio.event
        async def disconnect(sid):
            print(f"❌ Client disconnected: {sid}")
        
        @self.sio.event
        async def request_data(sid, data):
            """Handle client data requests"""
            data_type = data.get('type')
            if data_type == 'detections':
                await self.sio.emit('detection_history', {
                    'detections': list(self.recent_detections)
                }, room=sid)
            elif data_type == 'logs':
                await self.sio.emit('log_history', {
                    'logs': list(self.recent_logs)
                }, room=sid)
    
    async def _send_initial_data(self, sid: str):
        """Send initial data to newly connected client"""
        # Send recent detections
        if self.recent_detections:
            await self.sio.emit('detection_history', {
                'detections': list(self.recent_detections)
            }, room=sid)
        
        # Send recent logs
        if self.recent_logs:
            await self.sio.emit('log_history', {
                'logs': list(self.recent_logs)
            }, room=sid)
        
        # Send active alerts
        if self.active_alerts:
            for alert in self.active_alerts:
                await self.sio.emit('alert', alert, room=sid)
    
    async def broadcast_system_metrics(self, metrics: Dict[str, Any]):
        """Broadcast system metrics to all connected clients"""
        await self.sio.emit('system_metrics', metrics)
    
    async def broadcast_node_update(self, node_data: Dict[str, Any]):
        """Broadcast node status update"""
        await self.sio.emit('edge_node_update', node_data)
    
    async def broadcast_detection(self, detection: Dict[str, Any]):
        """Broadcast new detection result"""
        # Add timestamp if not present
        if 'timestamp' not in detection:
            detection['timestamp'] = datetime.utcnow().isoformat()
        
        # Store in recent detections
        self.recent_detections.append(detection)
        
        # Broadcast to all clients
        await self.sio.emit('detection_result', detection)
    
    async def broadcast_consensus_update(self, consensus_data: Dict[str, Any]):
        """Broadcast consensus round update"""
        await self.sio.emit('consensus_update', consensus_data)
    
    async def broadcast_log(self, log_entry: Dict[str, Any]):
        """Broadcast system log"""
        # Add timestamp if not present
        if 'timestamp' not in log_entry:
            log_entry['timestamp'] = datetime.utcnow().isoformat()
        
        # Store in recent logs
        self.recent_logs.append(log_entry)
        
        # Broadcast to all clients
        await self.sio.emit('system_log', log_entry)
    
    async def broadcast_alert(self, alert: Dict[str, Any]):
        """Broadcast system alert"""
        # Add timestamp if not present
        if 'timestamp' not in alert:
            alert['timestamp'] = datetime.utcnow().isoformat()
        
        # Store in active alerts
        self.active_alerts.append(alert)
        
        # Broadcast to all clients
        await self.sio.emit('alert', alert)
    
    def dismiss_alert(self, alert_id: int):
        """Remove alert from active alerts"""
        self.active_alerts = [a for a in self.active_alerts if a.get('id') != alert_id]
    
    async def start_metrics_broadcaster(self, db_getter):
        """Background task to broadcast metrics periodically"""
        from ..config import settings
        from .system_service import get_system_metrics
        
        while True:
            try:
                # Get database session
                db = next(db_getter())
                
                # Get current metrics
                metrics = await get_system_metrics(db)
                
                # Broadcast metrics
                await self.broadcast_system_metrics(metrics)
                
                # Close database session
                db.close()
                
                # Wait before next broadcast
                await asyncio.sleep(settings.METRICS_BROADCAST_INTERVAL)
                
            except Exception as e:
                print(f"❌ Error broadcasting metrics: {e}")
                await asyncio.sleep(settings.METRICS_BROADCAST_INTERVAL)


# Global WebSocket service instance
ws_service = WebSocketService()
