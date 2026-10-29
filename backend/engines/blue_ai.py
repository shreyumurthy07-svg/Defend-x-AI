import json
from backend.pipeline.schema import SecurityEvent

class BlueAI:
    """The Defender Engine: Detects and responds to threats."""
    
    def __init__(self):
        self.rules = {
            'brute_force_threshold': 5,
            'exfiltration_threshold': 1000000,
            'c2_ips': ['198.51.100.22']
        }
        self.history = []

    def analyze_event(self, event: SecurityEvent):
        metadata = event.metadata
        alert = None

        # Simple heuristic detection (to be replaced/augmented by ML)
        if event.event_type == 'network':
            if metadata.get('dst_ip') in self.rules['c2_ips']:
                alert = self._create_alert(event, "C2 Beaconing Detected", "High")
            
            elif metadata.get('bytes', 0) > self.rules['exfiltration_threshold']:
                alert = self._create_alert(event, "Data Exfiltration Suspected", "Critical")

        elif event.event_type == 'endpoint':
            if "powershell" in metadata.get('process', '').lower() and "net use" in metadata.get('activity', '').lower():
                alert = self._create_alert(event, "Lateral Movement Attempt", "Medium")

        if alert:
            self.take_action(alert)
        
        return alert

    def _create_alert(self, trigger_event: SecurityEvent, reason: str, severity: str):
        return {
            "alert_id": f"ALRT-{trigger_event.timestamp}",
            "reason": reason,
            "severity": severity,
            "confidence": 0.85,
            "trigger_event": trigger_event.to_dict(),
            "explainability": f"Detected based on {reason}. Resource: {trigger_event.source}."
        }

    def take_action(self, alert):
        print(f"[Blue AI] ACTION TAKEN: {alert['severity']} Alert - {alert['reason']}")
        # In a real system, this would call firewall APIs or endpoint agents
        if alert['severity'] == "Critical":
            print(f"Blocking source IP: {alert['trigger_event']['metadata'].get('src_ip')}")

if __name__ == "__main__":
    blue = BlueAI()
    # Mocking an event
    from backend.pipeline.schema import create_network_event
    test_event = create_network_event("10.0.0.10", "198.51.100.22", 8080, "HTTP", 100)
    alert = blue.analyze_event(test_event)
    if alert:
        print(json.dumps(alert, indent=2))
