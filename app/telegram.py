import html, requests
from .config import settings
def esc(v): return html.escape(str(v), quote=False)
def api_url(method): return f'https://api.telegram.org/bot{settings.telegram_bot_token}/{method}'
def send_message(text, chat_id=None, disable_web_page_preview=False):
    target=chat_id or settings.telegram_chat_id
    r=requests.post(api_url('sendMessage'),json={'chat_id':target,'text':text,'parse_mode':'HTML','disable_web_page_preview':disable_web_page_preview},timeout=15)
    r.raise_for_status(); return r.json()
def set_webhook():
    url=f"{settings.app_public_url.rstrip('/')}/telegram/{settings.webhook_secret}"
    r=requests.post(api_url('setWebhook'),json={'url':url,'drop_pending_updates':True},timeout=20); r.raise_for_status(); return r.json()
def delete_webhook():
    r=requests.post(api_url('deleteWebhook'),json={'drop_pending_updates':True},timeout=20); r.raise_for_status(); return r.json()
