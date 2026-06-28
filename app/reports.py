from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from .config import settings
from .storage import daily_summary, report_sent, mark_report_sent, get_str_config
from .telegram import send_message, esc

def fmt_duration(s): s=int(s or 0); return f'{s//3600}h {(s%3600)//60}m'
def report_text(day):
    tz=ZoneInfo(settings.timezone); start=datetime(day.year,day.month,day.day,tzinfo=tz); end=start+timedelta(days=1); s=daily_summary(int(start.timestamp()),int(end.timestamp()))
    return f"📊 <b>Daily Teltonika Report</b>\nDevice: <b>{esc(settings.device_name)}</b>\nDate: <b>{day.isoformat()}</b>\n\nIdling time: <b>{fmt_duration(s['idle_sec'])}</b>\nAverage trip time: <b>{fmt_duration(s['avg_trip_sec'])}</b>\nNumber of trips: <b>{s['trip_count']}</b>"
def send_report(day): send_message(report_text(day), disable_web_page_preview=True)
def maybe_send_daily_report():
    tz=ZoneInfo(settings.timezone); now=datetime.now(tz); rt=get_str_config('daily_report_time',settings.daily_report_time)
    if now.strftime('%H:%M')!=rt: return
    d=now.date()-timedelta(days=1); key=d.isoformat()
    if report_sent(key): return
    send_report(d); mark_report_sent(key)
