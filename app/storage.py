import os, sqlite3
from contextlib import contextmanager
from datetime import datetime
from .config import settings
os.makedirs(os.path.dirname(settings.sqlite_path), exist_ok=True)
@contextmanager
def db():
    con = sqlite3.connect(settings.sqlite_path)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()

def init_db():
    with db() as con:
        con.executescript('''
        CREATE TABLE IF NOT EXISTS telemetry (id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT, ts INTEGER, lat REAL, lon REAL, speed REAL, ignition INTEGER, towing INTEGER, raw TEXT);
        CREATE TABLE IF NOT EXISTS device_state (device_id TEXT PRIMARY KEY, last_ts INTEGER, last_lat REAL, last_lon REAL, last_speed REAL, last_ignition INTEGER, last_location_sent_ts INTEGER, trip_open INTEGER DEFAULT 0, trip_start_ts INTEGER, idle_start_ts INTEGER, last_towing_ts INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS trips (id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT, start_ts INTEGER, end_ts INTEGER, duration_sec INTEGER);
        CREATE TABLE IF NOT EXISTS idle_periods (id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT, start_ts INTEGER, end_ts INTEGER, duration_sec INTEGER);
        CREATE TABLE IF NOT EXISTS daily_reports (report_date TEXT PRIMARY KEY, sent_at TEXT);
        CREATE TABLE IF NOT EXISTS runtime_config (key TEXT PRIMARY KEY, value TEXT, updated_at TEXT);
        ''')

def get_state(device_id):
    with db() as con:
        row = con.execute("SELECT * FROM device_state WHERE device_id=?", (device_id,)).fetchone()
        return dict(row) if row else None

def upsert_state(device_id, **kwargs):
    current = get_state(device_id) or {"device_id": device_id}
    current.update(kwargs)
    columns = ["device_id","last_ts","last_lat","last_lon","last_speed","last_ignition","last_location_sent_ts","trip_open","trip_start_ts","idle_start_ts","last_towing_ts"]
    values = [current.get(c) for c in columns]
    with db() as con:
        con.execute(f"INSERT INTO device_state ({','.join(columns)}) VALUES ({','.join(['?']*len(columns))}) ON CONFLICT(device_id) DO UPDATE SET {','.join([f'{c}=excluded.{c}' for c in columns[1:]])}", values)

def insert_telemetry(device_id, ts, lat, lon, speed, ignition, towing, raw):
    with db() as con:
        con.execute("INSERT INTO telemetry(device_id,ts,lat,lon,speed,ignition,towing,raw) VALUES(?,?,?,?,?,?,?,?)", (device_id, ts, lat, lon, speed, int(bool(ignition)), int(bool(towing)), raw))

def insert_trip(device_id, start_ts, end_ts):
    duration = max(0, end_ts - start_ts)
    if duration < settings.trip_min_duration_sec: return
    with db() as con:
        con.execute("INSERT INTO trips(device_id,start_ts,end_ts,duration_sec) VALUES(?,?,?,?)", (device_id,start_ts,end_ts,duration))

def insert_idle(device_id, start_ts, end_ts):
    duration = max(0, end_ts - start_ts)
    if duration <= 0: return
    with db() as con:
        con.execute("INSERT INTO idle_periods(device_id,start_ts,end_ts,duration_sec) VALUES(?,?,?,?)", (device_id,start_ts,end_ts,duration))

def daily_summary(start_ts, end_ts):
    with db() as con:
        trips = con.execute("SELECT COUNT(*) c, AVG(duration_sec) avg_sec FROM trips WHERE start_ts>=? AND start_ts<?", (start_ts,end_ts)).fetchone()
        idle = con.execute("SELECT COALESCE(SUM(duration_sec),0) total FROM idle_periods WHERE start_ts>=? AND start_ts<?", (start_ts,end_ts)).fetchone()
        return {"trip_count": trips["c"] or 0, "avg_trip_sec": int(trips["avg_sec"] or 0), "idle_sec": int(idle["total"] or 0)}

def report_sent(report_date: str):
    with db() as con:
        return con.execute("SELECT 1 FROM daily_reports WHERE report_date=?", (report_date,)).fetchone() is not None

def mark_report_sent(report_date: str):
    with db() as con:
        con.execute("INSERT OR REPLACE INTO daily_reports(report_date,sent_at) VALUES(?,?)", (report_date, datetime.utcnow().isoformat()+"Z"))


def set_config(key: str, value: str):
    with db() as con:
        con.execute("INSERT OR REPLACE INTO runtime_config(key,value,updated_at) VALUES(?,?,?)", (key, str(value), datetime.utcnow().isoformat()+"Z"))

def get_config(key: str, default=None):
    with db() as con:
        row = con.execute("SELECT value FROM runtime_config WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default

def get_int_config(key: str, default: int):
    value = get_config(key, None)
    try:
        return int(value) if value is not None else int(default)
    except Exception:
        return int(default)

def get_str_config(key: str, default: str):
    value = get_config(key, None)
    return str(value) if value is not None else str(default)
