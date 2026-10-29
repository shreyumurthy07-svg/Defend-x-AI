:root {
    --bg-color: #05070a;
    --card-bg: rgba(15, 20, 28, 0.7);
    --border-color: rgba(0, 255, 255, 0.1);
    --primary-cyan: #00f2ff;
    --primary-blue: #0072ff;
    --alert-high: #ff0055;
    --alert-medium: #ffaa00;
    --alert-low: #00ffaa;
    --text-main: #e0e6ed;
    --text-dim: #94a3b8;
    --glass: blur(10px);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

body {
    background-color: var(--bg-color);
    color: var(--text-main);
    overflow: hidden;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

header {
    height: 70px;
    padding: 0 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-color);
    background: rgba(5, 7, 10, 0.8);
    backdrop-filter: var(--glass);
    z-index: 100;
}

.logo {
    font-size: 24px;
    font-weight: 800;
    background: linear-gradient(90deg, var(--primary-cyan), var(--primary-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}

.main-container {
    display: grid;
    grid-template-columns: 350px 1fr 350px;
    gap: 20px;
    padding: 20px;
    flex: 1;
    overflow: hidden;
}

.panel {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    backdrop-filter: var(--glass);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.panel-header {
    padding: 15px 20px;
    border-bottom: 1px solid var(--border-color);
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-dim);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.event-list, .alert-feed {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
}

.event-item {
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    background: rgba(255, 255, 255, 0.03);
    border-left: 3px solid var(--text-dim);
    font-size: 13px;
    transition: transform 0.2s;
}

.event-item:hover {
    transform: translateX(5px);
    background: rgba(255, 255, 255, 0.05);
}

.event-item.critical { border-left-color: var(--alert-high); }
.event-item.high { border-left-color: var(--alert-medium); }
.event-item.medium { border-left-color: var(--primary-blue); }

.badge {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: bold;
}

.badge-critical { background: rgba(255, 0, 85, 0.2); color: var(--alert-high); }
.badge-high { background: rgba(255, 170, 0, 0.2); color: var(--alert-medium); }

.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    padding: 20px;
}

.stat-card {
    background: rgba(255, 255, 255, 0.02);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

.stat-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--primary-cyan);
}

.stat-label {
    font-size: 11px;
    color: var(--text-dim);
}

/* Animations */
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.live-indicator {
    width: 8px;
    height: 8px;
    background: #00ff00;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 10px;
}
