from datetime import datetime
from .config import settings
from .telegram import send_message, esc
from .storage import get_state, upsert_state, insert_telemetry, insert_trip, insert_idle, get_int_config, get_float_config
def maps_links(lat,lon): return f'https://www.google.com/maps?q={lat},{lon}', f'https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}'
def fmt_ts(ts): return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
def process_telemetry(t):
    device_id,ts,lat,lon,speed,ignition,towing=t['device_id'],t['ts'],t['lat'],t['lon'],t['speed'],t['ignition'],t['towing']
    insert_telemetry(device_id,ts,lat,lon,speed,ignition,towing,t['raw'])
    st=get_state(device_id) or {}; old=st.get('last_ignition'); last_loc=st.get('last_location_sent_ts') or 0; trip_open=bool(st.get('trip_open') or 0); trip_start=st.get('trip_start_ts'); idle_start=st.get('idle_start_ts'); last_tow=st.get('last_towing_ts') or 0
    interval=get_int_config('location_interval_sec',settings.location_interval_sec); idle_speed=get_float_config('idle_speed_kmh',settings.idle_speed_kmh)
    if lat is not None and lon is not None and ts-last_loc>=interval:
        g,o=maps_links(lat,lon); send_message(f"📍 <b>{esc(settings.device_name)}</b>\nDevice: <code>{esc(device_id)}</code>\nIgnition: <b>{'ON' if ignition else 'OFF'}</b>\nSpeed: <b>{speed:.1f} km/h</b>\nTime: {esc(fmt_ts(ts))}\n\nGoogle Maps: {g}\nOpenStreetMap Live View: {o}"); last_loc=ts
    if old is not None and int(old)!=int(ignition): send_message(f"🔑 <b>Ignition changed</b>\nDevice: <code>{esc(device_id)}</code>\nStatus: <b>{'ON' if ignition else 'OFF'}</b>\nTime: {esc(fmt_ts(ts))}", disable_web_page_preview=True)
    if towing and ts-last_tow>600:
        text=f"🚨 <b>Towing Alert</b>\nDevice: <code>{esc(device_id)}</code>\nTime: {esc(fmt_ts(ts))}"
        if lat is not None and lon is not None:
            g,o=maps_links(lat,lon); text+=f"\nGoogle Maps: {g}\nOpenStreetMap: {o}"
        send_message(text); last_tow=ts
    if ignition and not trip_open: trip_open=True; trip_start=ts
    if not ignition and trip_open and trip_start: insert_trip(device_id,int(trip_start),ts); trip_open=False; trip_start=None
    is_idle=ignition and speed<=idle_speed
    if is_idle and not idle_start: idle_start=ts
    if (not is_idle) and idle_start: insert_idle(device_id,int(idle_start),ts); idle_start=None
    upsert_state(device_id,last_ts=ts,last_lat=lat,last_lon=lon,last_speed=speed,last_ignition=int(bool(ignition)),last_location_sent_ts=last_loc,trip_open=int(trip_open),trip_start_ts=trip_start,idle_start_ts=idle_start,last_towing_ts=last_tow)
