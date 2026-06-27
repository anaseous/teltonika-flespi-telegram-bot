import html, requests
from .config import settings

def send_telegram(text: str, disable_web_page_preview: bool = False):
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        raise RuntimeError("Telegram token or chat ID is missing. Check .env file.")
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {"chat_id": settings.telegram_chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": disable_web_page_preview}
    r = requests.post(url, json=payload, timeout=15)
    r.raise_for_status()
    return r.json()

def esc(value):
    return html.escape(str(value), quote=False)
