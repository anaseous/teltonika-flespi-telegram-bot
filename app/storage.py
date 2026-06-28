import os, sqlite3, hashlib, json
from contextlib import contextmanager
from datetime import datetime
from .config import settings
os.makedirs(os.path.dirname(settings.sqlite_path), exist_ok=True)
@contextmanager
def db():
    con=sqlite3.connect(settings.sqlite_path); con.row_factory=sqlite3.Row
    try:
        yield con; con.commit()
    finally:
        con.close()
def init_db():
    sql=("CREATE TABLE IF NOT EXISTS runtime_config (key TEXT PRIMARY KEY,value TEXT,updated_at TEXT);"
         "CREATE TABLE IF NOT EXISTS processed_messages (signature TEXT PRIMARY KEY, processed_at TEXT);"
         "CREATE TABLE IF NOT EXISTS telegram_state (id INTEGER PRIMARY KEY CHECK(id=1), offset INTEGER);"
         "CREATE TABLE IF NOT EXISTS telemetry (id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT, ts INTEGER, lat REAL, lon REAL, speed REAL, ignition INTEGER, towing INTEGER, raw TEXT);"
         "CREATE TABLE IF NOT EXISTS device_state (device_id TEXT PRIMARY KEY,last_ts INTEGER,last_lat REAL,last_lon REAL,last_speed REAL,last_ignition INTEGER,last_location_sent_ts INTEGER,trip_open INTEGER DEFAULT 0,trip_start_ts INTEGER,idle_start_ts INTEGER,last_towing_ts INTEGER DEFAULT 0);"
         "CREATE TABLE IF NOT EXISTS trips (id INTEGER PRIMARY KEY AUTOINCREMENT,device_id TEXT,start_ts INTEGER,end_ts INTEGER,duration_sec INTEGER);"
         "CREATE TABLE IF NOT EXISTS idle_periods (id INTEGER PRIMARY KEY AUTOINCREMENT,device_id TEXT,start_ts INTEGER,end_ts INTEGER,duration_sec INTEGER);"
         "CREATE TABLE IF NOT EXISTS daily_reports (report_date TEXT PRIMARY KEY,sent_at TEXT);")
    with db() as con:
        con.executescript(sql); con.execute('INSERT OR IGNORE INTO telegram_state(id,offset) VALUES(1,NULL)')
def signature(payload): return hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()
def is_processed(payload):
    with db() as con: return con.execute('SELECT 1 FROM processed_messages WHERE signature=?',(signature(payload),)).fetchone() is not None
def mark_processed(payload):
    with db() as con: con.execute('INSERT OR IGNORE INTO processed_messages(signature,processed_at) VALUES(?,?)',(signature(payload),datetime.utcnow().isoformat()+'Z'))
def set_config(k,v):
    with db() as con: con.execute('INSERT OR REPLACE INTO runtime_config(key,value,updated_at) VALUES(?,?,?)',(k,str(v),datetime.utcnow().isoformat()+'Z'))
def get_config(k,d=None):
    with db() as con:
        r=con.execute('SELECT value FROM runtime_config WHERE key=?',(k,)).fetchone(); return r['value'] if r else d
def get_int_config(k,d):
    try: return int(get_config(k,d))
    except Exception: return int(d)
def get_float_config(k,d):
    try: return float(get_config(k,d))
    except Exception: return float(d)
def get_str_config(k,d): return str(get_config(k,d))
def get_offset():
    with db() as con:
        r=con.execute('SELECT offset FROM telegram_state WHERE id=1').fetchone(); return r['offset'] if r and r['offset'] is not None else None
def set_offset(offset):
    with db() as con: con.execute('UPDATE telegram_state SET offset=? WHERE id=1',(offset,))
def get_state(device_id):
    with db() as con:
        r=con.execute('SELECT * FROM device_state WHERE device_id=?',(device_id,)).fetchone(); return dict(r) if r else None
def upsert_state(device_id, **kw):
    cur=get_state(device_id) or {'device_id':device_id}; cur.update(kw)
    cols=['device_id','last_ts','last_lat','last_lon','last_speed','last_ignition','last_location_sent_ts','trip_open','trip_start_ts','idle_start_ts','last_towing_ts']; vals=[cur.get(c) for c in cols]
    with db() as con: con.execute(f"INSERT INTO device_state ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))}) ON CONFLICT(device_id) DO UPDATE SET {','.join([f'{c}=excluded.{c}' for c in cols[1:]])}", vals)
def insert_telemetry(device_id,ts,lat,lon,speed,ignition,towing,raw):
    with db() as con: con.execute('INSERT INTO telemetry(device_id,ts,lat,lon,speed,ignition,towing,raw) VALUES(?,?,?,?,?,?,?,?)',(device_id,ts,lat,lon,speed,int(bool(ignition)),int(bool(towing)),raw))
def insert_trip(device_id,start_ts,end_ts):
    dur=max(0,end_ts-start_ts)
    if dur<get_int_config('trip_min_duration_sec',settings.trip_min_duration_sec): return
    with db() as con: con.execute('INSERT INTO trips(device_id,start_ts,end_ts,duration_sec) VALUES(?,?,?,?)',(device_id,start_ts,end_ts,dur))
def insert_idle(device_id,start_ts,end_ts):
    dur=max(0,end_ts-start_ts)
    if dur<=0: return
    with db() as con: con.execute('INSERT INTO idle_periods(device_id,start_ts,end_ts,duration_sec) VALUES(?,?,?,?)',(device_id,start_ts,end_ts,dur))
def daily_summary(start_ts,end_ts):
    with db() as con:
        tr=con.execute('SELECT COUNT(*) c, AVG(duration_sec) a FROM trips WHERE start_ts>=? AND start_ts<?',(start_ts,end_ts)).fetchone(); idle=con.execute('SELECT COALESCE(SUM(duration_sec),0) t FROM idle_periods WHERE start_ts>=? AND start_ts<?',(start_ts,end_ts)).fetchone(); return {'trip_count':tr['c'] or 0,'avg_trip_sec':int(tr['a'] or 0),'idle_sec':int(idle['t'] or 0)}
def report_sent(day):
    with db() as con: return con.execute('SELECT 1 FROM daily_reports WHERE report_date=?',(day,)).fetchone() is not None
def mark_report_sent(day):
    with db() as con: con.execute('INSERT OR REPLACE INTO daily_reports(report_date,sent_at) VALUES(?,?)',(day,datetime.utcnow().isoformat()+'Z'))
