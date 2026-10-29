// SOC Dashboard Logic
document.addEventListener('DOMContentLoaded', () => {
    const eventStream = document.getElementById('event-stream');
    const alertFeed = document.getElementById('alert-feed');
    const epsCounter = document.getElementById('eps-counter');
    const learningProgress = document.getElementById('learning-progress');
    const shadowInsight = document.getElementById('shadow-insight');

    // Stats
    let totalEvents = 0;
    let totalAlerts = 0;

    // Initialize Chart
    const ctx = document.getElementById('threat-chart').getContext('2d');
    const threatChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array(20).fill(''),
            datasets: [{
                label: 'Red AI Attack Velocity',
                data: Array(20).fill(0),
                borderColor: '#ff0055',
                backgroundColor: 'rgba(255, 0, 85, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Blue AI Block Rate',
                data: Array(20).fill(0),
                borderColor: '#00f2ff',
                backgroundColor: 'rgba(0, 242, 255, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { display: false },
                x: { display: false }
            },
            plugins: {
                legend: { labels: { color: '#94a3b8', font: { size: 10 } } }
            },
            animation: { duration: 0 }
        }
    });

    // Clock update
    setInterval(() => {
        document.getElementById('clock').innerText = new Date().toISOString().split('T')[1].split('.')[0] + " UTC";
    }, 1000);

    function addEvent(data) {
        const item = document.createElement('div');
        item.className = `event_item ${data.severity?.toLowerCase() || ''}`;
        item.innerHTML = `
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="color: var(--primary-cyan); font-weight: 600;">${data.event_type.toUpperCase()}</span>
                <span style="font-size: 10px; color: var(--text-dim);">${data.timestamp.split('T')[1].split('.')[0]}</span>
            </div>
            <div style="color: var(--text-main); font-family: 'JetBrains Mono'; font-size: 11px;">
                SRC: ${data.metadata.src_ip || 'Internal'} -> DST: ${data.metadata.dst_ip || 'Internal'}
            </div>
        `;
        eventStream.prepend(item);
        if (eventStream.children.length > 50) eventStream.removeChild(eventStream.lastChild);
        
        totalEvents++;
        epsCounter.innerText = `${500 + Math.floor(Math.random() * 50)} EPS`;
    }

    function addAlert(alert) {
        if (!alert) return;
        const item = document.createElement('div');
        item.className = 'event-item';
        item.style.background = 'rgba(255, 0, 85, 0.05)';
        item.style.borderLeft = '3px solid var(--alert-high)';
        item.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge badge-critical">${alert.severity}</span>
                <span style="font-size: 11px; font-weight: bold; color: var(--alert-high);">${alert.reason}</span>
            </div>
            <p style="font-size: 11px; margin-top: 8px; color: var(--text-dim);">${alert.explainability}</p>
            <div style="margin-top: 8px; display: flex; gap: 10px;">
                <button class="badge" style="background: var(--alert-high); color: white; border: none; cursor: pointer;">ISOLATE</button>
                <button class="badge" style="background: rgba(255,255,255,0.1); color: white; border: none; cursor: pointer;">PCAP</button>
            </div>
        `;
        alertFeed.prepend(item);
        if (alertFeed.children.length > 20) alertFeed.removeChild(alertFeed.lastChild);
        totalAlerts++;
    }

    // WebSocket Connection
    let socket;
    function connectWS() {
        socket = new WebSocket('ws://localhost:8000/ws/alerts');
        
        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            addEvent(data.event);
            if (data.alert) addAlert(data.alert);
            
            // Update Chart
            threatChart.data.datasets[0].data.shift();
            threatChart.data.datasets[0].data.push(Math.random() * 100);
            threatChart.data.datasets[1].data.shift();
            threatChart.data.datasets[1].data.push(data.alert ? 80 + Math.random() * 20 : 0);
            threatChart.update();

            // Shadow Learning Update
            const score = data.system_status.shadow_learning_score;
            learningProgress.style.width = `${Math.min(100, score * 5)}%`;
        };

        socket.onclose = () => {
            console.log("Reconnecting in 5s...");
            setTimeout(connectWS, 5000);
        };
    }

    // Mock Data Generator (if backend not connected)
    function startMockData() {
        console.log("Backend not detected. Running in SIMULATION MODE...");
        setInterval(() => {
            if (socket && socket.readyState === WebSocket.OPEN) return;
            
            const isAttack = Math.random() > 0.7;
            const mockEvent = {
                timestamp: new Date().toISOString(),
                event_type: isAttack ? 'network' : 'endpoint',
                severity: isAttack ? 'High' : 'Low',
                metadata: {
                    src_ip: isAttack ? '203.0.113.45' : '10.0.0.5',
                    dst_ip: '10.0.0.10',
                    activity: isAttack ? 'C2 Beaconing' : 'Normal file access'
                }
            };
            addEvent(mockEvent);

            if (isAttack) {
                const mockAlert = {
                    severity: 'High',
                    reason: 'C2 Communication Detected',
                    explainability: 'Detected periodic beaconing to known malicious infrastructure IP: 203.0.113.45.',
                    confidence: 0.94
                };
                addAlert(mockAlert);
            }

            // Update Chart
            threatChart.data.datasets[0].data.shift();
            threatChart.data.datasets[0].data.push(isAttack ? 80 + Math.random() * 20 : 20 + Math.random() * 10);
            threatChart.data.datasets[1].data.shift();
            threatChart.data.datasets[1].data.push(isAttack ? 70 + Math.random() * 30 : 0);
            threatChart.update();
        }, 1000);
    }

    connectWS();
    startMockData(); // Always run as fallback
});
