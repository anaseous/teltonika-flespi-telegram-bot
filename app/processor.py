from datetime import datetime
from .config import settings
from .telegram import send_telegram, esc
from .storage import get_state, upsert_state, insert_telemetry, insert_trip, insert_idle, get_int_config

def maps_links(lat, lon):
    return f"https://www.google.com/maps?q={lat},{lon}", f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}"

def fmt_ts(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def process_telemetry(t):
    device_id, ts, lat, lon, speed, ignition, towing = t["device_id"], t["ts"], t["lat"], t["lon"], t["speed"], t["ignition"], t["towing"]
    insert_telemetry(device_id, ts, lat, lon, speed, ignition, towing, t["raw"])
    st = get_state(device_id) or {}
    old_ignition = st.get("last_ignition")
    last_location_sent_ts = st.get("last_location_sent_ts") or 0
    trip_open = bool(st.get("trip_open") or 0)
    trip_start_ts = st.get("trip_start_ts")
    idle_start_ts = st.get("idle_start_ts")
    last_towing_ts = st.get("last_towing_ts") or 0
    messages=[]
    location_interval = get_int_config("location_interval_sec", settings.location_send_interval_sec)
    if lat is not None and lon is not None:
        if settings.send_location_on_every_message or (ts-last_location_sent_ts >= location_interval):
            google, osm = maps_links(lat, lon)
            text = f"📍 <b>{esc(settings.device_name)}</b> location update\nDevice: <code>{esc(device_id)}</code>\nIgnition: <b>{'ON' if ignition else 'OFF'}</b>\nSpeed: <b>{speed:.1f} km/h</b>\nTime: {esc(fmt_ts(ts))}\n\nGoogle Maps: {google}\nOpenStreetMap Live View: {osm}"
            messages.append((text, False))
            last_location_sent_ts = ts
    if settings.send_ignition_change and old_ignition is not None and int(old_ignition) != int(ignition):
        text = f"🔑 <b>Ignition changed</b>\nDevice: <code>{esc(device_id)}</code>\nStatus: <b>{'ON' if ignition else 'OFF'}</b>\nTime: {esc(fmt_ts(ts))}"
        messages.append((text, True))
    if settings.send_towing_alert and towing and ts-last_towing_ts > 600:
        text = f"🚨 <b>Towing Alert</b>\nDevice: <code>{esc(device_id)}</code>\nTime: {esc(fmt_ts(ts))}"
        if lat is not None and lon is not None:
            google, osm = maps_links(lat, lon)
            text += f"\nGoogle Maps: {google}\nOpenStreetMap: {osm}"
        messages.append((text, False)); last_towing_ts = ts
    if ignition and not trip_open:
        trip_open=True; trip_start_ts=ts
    if not ignition and trip_open and trip_start_ts:
        insert_trip(device_id, int(trip_start_ts), ts); trip_open=False; trip_start_ts=None
    is_idle = ignition and speed <= settings.idle_speed_kmh
    if is_idle and not idle_start_ts: idle_start_ts=ts
    if (not is_idle) and idle_start_ts:
        insert_idle(device_id, int(idle_start_ts), ts); idle_start_ts=None
    upsert_state(device_id, last_ts=ts, last_lat=lat, last_lon=lon, last_speed=speed, last_ignition=int(bool(ignition)), last_location_sent_ts=last_location_sent_ts, trip_open=int(trip_open), trip_start_ts=trip_start_ts, idle_start_ts=idle_start_ts, last_towing_ts=last_towing_ts)
    for msg, disable_preview in messages: send_telegram(msg, disable_web_page_preview=disable_preview)
