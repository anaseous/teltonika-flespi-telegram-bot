from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from .config import settings
from .storage import daily_summary, report_sent, mark_report_sent, get_str_config
from .telegram import send_telegram, esc

def fmt_duration(seconds):
    seconds=int(seconds or 0); return f"{seconds//3600}h {(seconds%3600)//60}m"

def maybe_send_daily_report():
    tz=ZoneInfo(settings.timezone); now=datetime.now(tz)
    report_time = get_str_config("daily_report_time", settings.daily_report_time)
    if now.strftime("%H:%M") != report_time: return
    previous_day=now.date()-timedelta(days=1); key=previous_day.isoformat()
    if report_sent(key): return
    start=datetime(previous_day.year, previous_day.month, previous_day.day, tzinfo=tz); end=start+timedelta(days=1)
    s=daily_summary(int(start.timestamp()), int(end.timestamp()))
    text=f"📊 <b>Daily Teltonika Report</b>\nDevice: <b>{esc(settings.device_name)}</b>\nDate: <b>{key}</b>\n\nIdling time: <b>{fmt_duration(s['idle_sec'])}</b>\nAverage trip time: <b>{fmt_duration(s['avg_trip_sec'])}</b>\nNumber of trips: <b>{s['trip_count']}</b>"
    send_telegram(text, disable_web_page_preview=True); mark_report_sent(key)
