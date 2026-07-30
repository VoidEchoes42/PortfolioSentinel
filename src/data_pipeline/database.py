import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "risk_database.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initializes the SQLite database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_snapshots (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_exposure REAL,
            portfolio_var_95 REAL,
            expected_credit_loss REAL,
            active_alerts INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alert_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            category TEXT,
            severity TEXT,
            message TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def log_risk_snapshot(exposure: float, var_95: float, expected_loss: float, alerts_count: int):
    """Saves a daily snapshot of key risk metrics."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO risk_snapshots (total_exposure, portfolio_var_95, expected_credit_loss, active_alerts) VALUES (?, ?, ?, ?)",
        (exposure, var_95, expected_loss, alerts_count)
    )
    conn.commit()
    conn.close()

def log_alerts(alerts: list):
    """Logs generated alerts into the database."""
    if not alerts: return
    conn = get_connection()
    cursor = conn.cursor()
    
    for alert in alerts:
        cursor.execute(
            "INSERT INTO alert_history (timestamp, category, severity, message) VALUES (?, ?, ?, ?)",
            (alert['timestamp'], alert['category'], alert['severity'], alert['message'])
        )
        
    conn.commit()
    conn.close()

def load_alert_history():
    """Loads historical alerts."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM alert_history ORDER BY timestamp DESC", conn)
    conn.close()
    return df
