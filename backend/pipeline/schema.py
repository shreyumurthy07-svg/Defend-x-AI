import json
from datetime import datetime
from typing import Dict, Any, Optional

class SecurityEvent:
    """Standardized schema for all security logs (Network, Endpoint, App)."""
    
    def __init__(
        self,
        event_type: str,  # 'network', 'endpoint', 'app'
        source: str,
        severity: str = 'Low',
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.timestamp = datetime.utcnow().isoformat()
        self.event_type = event_type
        self.source = source
        self.severity = severity
        self.confidence = confidence
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "source": self.source,
            "severity": self.severity,
            "confidence": self.confidence,
            "metadata": self.metadata
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

def create_network_event(src_ip: str, dst_ip: str, port: int, protocol: str, bytes_sent: int) -> SecurityEvent:
    return SecurityEvent(
        event_type='network',
        source='firewall-01',
        metadata={
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "port": port,
            "protocol": protocol,
            "bytes": bytes_sent
        }
    )

def create_endpoint_event(process_name: str, pid: int, user: str, activity: str) -> SecurityEvent:
    return SecurityEvent(
        event_type='endpoint',
        source='host-agent-win10',
        metadata={
            "process": process_name,
            "pid": pid,
            "user": user,
            "activity": activity
        }
    )
