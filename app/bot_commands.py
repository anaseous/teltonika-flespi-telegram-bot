import re
import time
import requests
from .config import settings
from .telegram import send_telegram
from .storage import set_config, get_int_config, get_str_config

DURATION_RE = re.compile(r"^(\d+)(s|sec|m|min|h|hour|hours)$", re.IGNORECASE)
TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


def parse_duration(value: str):
    value = value.strip().lower()
    if value in ["off", "disable", "disabled"]:
        return 999999999
    m = DURATION_RE.match(value)
    if not m:
        return None
    number = int(m.group(1))
    unit = m.group(2)
    if unit in ["s", "sec"]:
        seconds = number
    elif unit in ["m", "min"]:
        seconds = number * 60
    else:
        seconds = number * 3600
    if seconds < 30:
        seconds = 30
    return seconds


def seconds_to_text(seconds: int):
    if seconds >= 999999999:
        return "OFF"
    if seconds % 3600 == 0:
        return f"{seconds // 3600}h"
    if seconds % 60 == 0:
        return f"{seconds // 60}min"
    return f"{seconds}s"


def send_help():
    interval = get_int_config("location_interval_sec", settings.location_send_interval_sec)
    daily_time = get_str_config("daily_report_time", settings.daily_report_time)
    text = (
        "🤖 <b>Teltonika Telegram Control</b>\n\n"
        "Use these commands from Telegram:\n\n"
        "<code>/settings</code> - show current settings\n"
        "<code>/interval 5min</code> - send location every 5 minutes\n"
        "<code>/interval 15min</code> - send location every 15 minutes\n"
        "<code>/interval 1h</code> - send location every 1 hour\n"
        "<code>/interval off</code> - disable scheduled location messages\n"
        "<code>/daily 00:00</code> - set daily report time\n"
        "<code>/help</code> - show this help\n\n"
        f"Current location interval: <b>{seconds_to_text(interval)}</b>\n"
        f"Current daily report time: <b>{daily_time}</b>"
    )
    send_telegram(text, disable_web_page_preview=True)


def process_command(text: str):
    text = (text or "").strip()
    if not text:
        return
    parts = text.split()
    cmd = parts[0].split('@')[0].lower()

    if cmd in ["/start", "/help"]:
        send_help()
        return

    if cmd == "/settings":
        interval = get_int_config("location_interval_sec", settings.location_send_interval_sec)
        daily_time = get_str_config("daily_report_time", settings.daily_report_time)
        send_telegram(
            "⚙️ <b>Current Settings</b>\n"
            f"Location interval: <b>{seconds_to_text(interval)}</b>\n"
            f"Daily report time: <b>{daily_time}</b>\n"
            f"Timezone: <b>{settings.timezone}</b>",
            disable_web_page_preview=True
        )
        return

    if cmd == "/interval":
        if len(parts) < 2:
            send_telegram("Please use: <code>/interval 5min</code>, <code>/interval 15min</code>, <code>/interval 1h</code>, or <code>/interval off</code>", True)
            return
        seconds = parse_duration(parts[1])
        if seconds is None:
            send_telegram("Invalid interval. Examples: <code>/interval 5min</code>, <code>/interval 30min</code>, <code>/interval 1h</code>, <code>/interval off</code>", True)
            return
        set_config("location_interval_sec", str(seconds))
        send_telegram(f"✅ Location interval updated to <b>{seconds_to_text(seconds)}</b>.", True)
        return

    if cmd == "/daily":
        if len(parts) < 2 or not TIME_RE.match(parts[1]):
            send_telegram("Please use 24-hour format, example: <code>/daily 00:00</code> or <code>/daily 23:30</code>", True)
            return
        set_config("daily_report_time", parts[1])
        send_telegram(f"✅ Daily report time updated to <b>{parts[1]}</b> timezone <b>{settings.timezone}</b>.", True)
        return

    send_telegram("Unknown command. Send <code>/help</code> to see available commands.", True)


def polling_loop():
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        print("Telegram command polling disabled: missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return
    offset = None
    base_url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/getUpdates"
    print("Telegram command polling started.")
    while True:
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset
            response = requests.get(base_url, params=params, timeout=40)
            response.raise_for_status()
            data = response.json()
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message") or update.get("edited_message") or {}
                chat = message.get("chat", {})
                chat_id = str(chat.get("id", ""))
                if chat_id != str(settings.telegram_chat_id):
                    continue
                process_command(message.get("text", ""))
        except Exception as exc:
            print(f"Telegram command polling error: {exc}")
            time.sleep(5)
