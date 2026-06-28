import re
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from .config import settings
from .telegram import send_message
from .storage import set_config, get_int_config, get_str_config
from .flespi import get_latest_messages
from .normalizer import normalize
from .processor import maps_links
from .reports import send_report

DURATION_RE=re.compile(r'^(\d+)(s|sec|m|min|h|hour|hours)$',re.I)
TIME_RE=re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')

def parse_duration(v):
    v=v.lower().strip()
    if v in ['off','disable','disabled']:
        return 999999999
    m=DURATION_RE.match(v)
    if not m:
        return None
    n=int(m.group(1)); u=m.group(2).lower()
    return max(n if u in ['s','sec'] else n*60 if u in ['m','min'] else n*3600,30)

def txt_sec(s):
    s=int(s)
    if s>=999999999:
        return 'OFF'
    if s%3600==0:
        return f'{s//3600}h'
    if s%60==0:
        return f'{s//60}min'
    return f'{s}s'

def help_text():
    i=get_int_config('location_interval_sec',settings.location_interval_sec)
    d=get_str_config('daily_report_time',settings.daily_report_time)
    return f"🤖 <b>Teltonika Flespi Telegram Bot</b>\n\nCommands:\n<code>/status</code> - latest status\n<code>/location</code> - latest map links\n<code>/settings</code> - current settings\n<code>/interval 5min</code> - set location interval\n<code>/interval 1h</code> - set location interval\n<code>/interval off</code> - stop periodic locations\n<code>/daily 00:00</code> - set daily report time\n<code>/report yesterday</code> - send report\n\nCurrent interval: <b>{txt_sec(i)}</b>\nDaily report: <b>{d}</b>"

def latest_normalized():
    m=get_latest_messages(1)
    return normalize(m[0]) if m else None

def handle_command(text,chat_id):
    parts=(text or '').strip().split()
    cmd=parts[0].split('@')[0].lower() if parts else ''
    if cmd in ['/start','/help']:
        send_message(help_text(),chat_id,True)
        return {'ok':True}
    if cmd=='/settings':
        send_message(help_text(),chat_id,True)
        return {'ok':True}
    if cmd=='/interval':
        if len(parts)<2:
            send_message('Use: <code>/interval 5min</code> or <code>/interval off</code>',chat_id,True)
            return {'ok':True}
        sec=parse_duration(parts[1])
        if sec is None:
            send_message('Invalid interval. Example: <code>/interval 5min</code>',chat_id,True)
            return {'ok':True}
        set_config('location_interval_sec',str(sec))
        send_message(f'✅ Location interval updated to <b>{txt_sec(sec)}</b>.',chat_id,True)
        return {'ok':True}
    if cmd=='/daily':
        if len(parts)<2 or not TIME_RE.match(parts[1]):
            send_message('Use: <code>/daily 00:00</code>',chat_id,True)
            return {'ok':True}
        set_config('daily_report_time',parts[1])
        send_message(f'✅ Daily report time updated to <b>{parts[1]}</b> ({settings.timezone}).',chat_id,True)
        return {'ok':True}
    if cmd in ['/status','/location']:
        latest=latest_normalized()
        if not latest:
            send_message('No Flespi telemetry found yet.',chat_id,True)
            return {'ok':True}
        links=''
        if latest['lat'] is not None and latest['lon'] is not None:
            g,o=maps_links(latest['lat'],latest['lon'])
            links=f"\nGoogle Maps: {g}\nOpenStreetMap: {o}"
        send_message(f"📡 <b>Latest Status</b>\nDevice: <code>{latest['device_id']}</code>\nIgnition: <b>{'ON' if latest['ignition'] else 'OFF'}</b>\nSpeed: <b>{latest['speed']:.1f} km/h</b>{links}",chat_id,False)
        return {'ok':True}
    if cmd=='/report':
        tz=ZoneInfo(settings.timezone)
        day=datetime.now(tz).date()
        if len(parts)>1 and parts[1].lower()=='yesterday':
            day=day-timedelta(days=1)
        send_report(day)
        return {'ok':True}
    send_message('Unknown command. Send <code>/help</code>.',chat_id,True)
    return {'ok':True}
