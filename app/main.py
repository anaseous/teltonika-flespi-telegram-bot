import time, threading
from .config import settings
from .storage import init_db, is_processed, mark_processed
from .telegram import get_updates, send_message
from .flespi import get_latest_messages
from .normalizer import normalize
from .processor import process_telemetry
from .commands import handle_command
from .reports import maybe_send_daily_report

def telegram_loop():
    print('Telegram long polling started. No webhook/domain required.')
    while True:
        try:
            for update in get_updates():
                msg=update.get('message') or update.get('edited_message') or {}; chat=str(msg.get('chat',{}).get('id',''))
                if str(settings.telegram_chat_id) and chat!=str(settings.telegram_chat_id): continue
                handle_command(msg.get('text',''),chat)
        except Exception as e:
            print('Telegram polling error:',e); time.sleep(5)

def flespi_loop():
    print('Flespi REST polling started.')
    while True:
        try:
            for payload in get_latest_messages(100):
                if is_processed(payload): continue
                process_telemetry(normalize(payload)); mark_processed(payload)
        except Exception as e: print('Flespi polling error:',e)
        time.sleep(settings.flespi_poll_interval_sec)

def daily_loop():
    while True:
        try: maybe_send_daily_report()
        except Exception as e: print('Daily report error:',e)
        time.sleep(30)

def main():
    init_db(); print('Starting Teltonika Flespi Telegram Bot - no webhook, no domain, no Docker.')
    try: send_message('✅ Teltonika Flespi Telegram Bot started. No webhook/domain/Docker required.', disable_web_page_preview=True)
    except Exception as e: print('Startup Telegram message failed:',e)
    threading.Thread(target=telegram_loop,daemon=True).start(); threading.Thread(target=daily_loop,daemon=True).start(); flespi_loop()
if __name__=='__main__': main()
