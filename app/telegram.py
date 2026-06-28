import html, requests
from .config import settings
from .storage import get_offset, set_offset

def esc(v): return html.escape(str(v), quote=False)
def api_url(method): return f'https://api.telegram.org/bot{settings.telegram_bot_token}/{method}'
def send_message(text, chat_id=None, disable_web_page_preview=False):
    target=chat_id or settings.telegram_chat_id
    r=requests.post(api_url('sendMessage'),json={'chat_id':target,'text':text,'parse_mode':'HTML','disable_web_page_preview':disable_web_page_preview},timeout=20)
    r.raise_for_status(); return r.json()
def get_updates():
    params={'timeout':settings.telegram_poll_timeout_sec,'limit':50}; offset=get_offset()
    if offset is not None: params['offset']=offset
    r=requests.get(api_url('getUpdates'),params=params,timeout=settings.telegram_poll_timeout_sec+10)
    r.raise_for_status(); updates=r.json().get('result',[])
    for u in updates: set_offset(int(u['update_id'])+1)
    return updates
