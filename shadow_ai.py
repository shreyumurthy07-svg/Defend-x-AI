import json
from collections import defaultdict
from backend.engines.blue_ai import BlueAI

class ShadowAI:
    """The Intelligence Engine: Learns from Red vs Blue and optimizes models."""
    
    def __init__(self, blue_ai: BlueAI):
        self.blue_ai = blue_ai
        self.agent_interactions = []
        self.user_risk_scores = defaultdict(float)

    def observe(self, attack_event, defense_alert):
        """Observe an interaction and adjust logic."""
        self.agent_interactions.append({
            "attack": attack_event.to_dict(),
            "defense": defense_alert
        })
        
        # Learn from Blue AI's performance
        if defense_alert and defense_alert['confidence'] < 0.9:
            print("[Shadow AI] Weak detection confidence. Analyzing for model adjustment...")
            # Simulate threshold optimization
            self._optimize_thresholds(attack_event)

    def calculate_insider_threat(self, user_id, activity_type):
        """Score users based on behavioral patterns."""
        risk_map = {
            "unusual_login": 20.0,
            "large_transfer": 50.0,
            "cmd_usage": 30.0
        }
        self.user_risk_scores[user_id] += risk_map.get(activity_type, 5.0)
        print(f"[Shadow AI] Insider Threat Score for {user_id}: {self.user_risk_scores[user_id]}")
        return self.user_risk_scores[user_id]

    def _optimize_thresholds(self, event):
        # Dynamically lower thresholds if attacks are being missed or have low confidence
        if event.event_type == 'network':
            self.blue_ai.rules['brute_force_threshold'] = max(2, self.blue_ai.rules['brute_force_threshold'] - 1)
            print(f"[Shadow AI] Adjusted Brute Force Threshold to: {self.blue_ai.rules['brute_force_threshold']}")

if __name__ == "__main__":
    from backend.pipeline.schema import create_network_event
    blue = BlueAI()
    shadow = ShadowAI(blue)
    
    # Observe missed attack/low confidence
    mock_attack = create_network_event("192.168.1.100", "10.0.0.5", 22, "TCP", 200)
    shadow.observe(mock_attack, None)
    
    # Observe user activity
    shadow.calculate_insider_threat("jsmith", "large_transfer")
