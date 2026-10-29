import asyncio
import json
from fastapi import FastAPI, WebSocket
from backend.engines.red_ai import RedAI
from backend.engines.blue_ai import BlueAI
from backend.engines.shadow_ai import ShadowAI
from backend.pipeline.correlation import CorrelationEngine

app = FastAPI(title="DefendX AI Backend")

# Initialize AI Engines
red_ai = RedAI()
blue_ai = BlueAI()
shadow_ai = ShadowAI(blue_ai)
correlation_engine = CorrelationEngine()

@app.get("/")
async def root():
    return {"status": "DefendX AI is Operational", "agents": ["RedAI", "BlueAI", "ShadowAI"]}

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[Server] Dashboard connected via WebSocket")
    
    try:
        while True:
            # Simulate real-time operation loop
            # 1. Red AI generates attacks
            events = red_ai.generate_attack()
            
            for event in events:
                # 2. Correlation Engine processes logs
                correlated_events = correlation_engine.correlate(event)
                
                for ce in correlated_events:
                    # 3. Blue AI attempts detection
                    alert = blue_ai.analyze_event(ce)
                    
                    # 4. Shadow AI observes and learns
                    shadow.observe(ce, alert)
                    
                    # 5. Send data to Dashboard
                    payload = {
                        "event": ce.to_dict(),
                        "alert": alert,
                        "system_status": {
                            "threat_level": "High" if alert and alert['severity'] in ['High', 'Critical'] else "Normal",
                            "shadow_learning_score": len(shadow.agent_interactions)
                        }
                    }
                    await websocket.send_text(json.dumps(payload))
                    await asyncio.sleep(0.5) # High throughput simulation
            
            await asyncio.sleep(2) # Pause between attack campaigns
    except Exception as e:
        print(f"[Server] WebSocket disconnected: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
