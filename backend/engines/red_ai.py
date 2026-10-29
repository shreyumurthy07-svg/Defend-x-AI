import random
import time
from backend.pipeline.schema import SecurityEvent, create_network_event, create_endpoint_event

class RedAI:
    """The Attacker Engine: Simulates cyberattacks and evolves patterns."""
    
    def __init__(self):
        self.attacks = ['brute_force', 'lateral_movement', 'data_exfiltration', 'c2_beaconing']
        self.attack_vectors = {
            'brute_force': self._simulate_brute_force,
            'lateral_movement': self._simulate_lateral_movement,
            'data_exfiltration': self._simulate_data_exfiltration,
            'c2_beaconing': self._simulate_c2_beaconing
        }

    def generate_attack(self):
        attack_type = random.choice(self.attacks)
        print(f"[Red AI] Launching {attack_type} attack simulation...")
        return self.attack_vectors[attack_type]()

    def _simulate_brute_force(self):
        events = []
        dst_ip = f"10.0.0.{random.randint(2, 254)}"
        for _ in range(10):  # Rapid login attempts
            events.append(create_network_event(
                src_ip="192.168.1.50",
                dst_ip=dst_ip,
                port=22,
                protocol="TCP",
                bytes_sent=random.randint(100, 500)
            ))
        return events

    def _simulate_lateral_movement(self):
        # Moving from one internal IP to another
        return [
            create_endpoint_event("powershell.exe", random.randint(1000, 9000), "SYSTEM", "net use \\\\10.0.0.5\\C$"),
            create_network_event("10.0.0.4", "10.0.0.5", 445, "SMB", random.randint(1000, 5000))
        ]

    def _simulate_data_exfiltration(self):
        # Large outbound transfer
        return [create_network_event(
            src_ip="10.0.0.10",
            dst_ip="203.0.113.45",
            port=443,
            protocol="HTTPS",
            bytes_sent=random.randint(1000000, 5000000)
        )]

    def _simulate_c2_beaconing(self):
        # Periodic small packets to a known malicious IP
        return [create_network_event(
            src_ip="10.0.0.10",
            dst_ip="198.51.100.22",
            port=8080,
            protocol="HTTP",
            bytes_sent=random.randint(50, 200)
        )]

if __name__ == "__main__":
    red = RedAI()
    while True:
        events = red.generate_attack()
        for e in events:
            print(e.to_json())
        time.sleep(5)
