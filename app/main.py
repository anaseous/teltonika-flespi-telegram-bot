import asyncio
from fastapi import FastAPI,Request,HTTPException
from .config import settings
from .storage import init_db
from .telegram import set_webhook, delete_webhook, send_message
from .normalizer import normalize
from .processor import process_telemetry
from .commands import handle_command
from .reports import maybe_send_daily_report
app=FastAPI(title='Teltonika Flespi Telegram Bot', version='2.0.0')
@app.on_event('startup')
async def startup(): init_db(); asyncio.create_task(daily_scheduler())
async def daily_scheduler():
    while True:
        try: maybe_send_daily_report()
        except Exception as e: print('Daily scheduler error:',e)
        await asyncio.sleep(30)
@app.get('/health')
def health(): return {'status':'ok','service':'teltonika-flespi-telegram-bot'}
@app.post('/telegram/{secret}')
async def telegram_webhook(secret:str,request:Request):
    if secret!=settings.webhook_secret: raise HTTPException(status_code=403,detail='Invalid webhook secret')
    update=await request.json(); msg=update.get('message') or update.get('edited_message') or {}; chat=msg.get('chat',{}); chat_id=str(chat.get('id',''))
    if str(settings.telegram_chat_id) and chat_id!=str(settings.telegram_chat_id): return {'ok':True,'ignored':'unauthorized chat'}
    return handle_command(msg.get('text',''),chat_id)
@app.post('/flespi/{secret}')
async def flespi_webhook(secret:str,request:Request):
    if secret!=settings.webhook_secret: raise HTTPException(status_code=403,detail='Invalid webhook secret')
    payload=await request.json(); messages=payload if isinstance(payload,list) else payload.get('messages',payload.get('result',[payload])) if isinstance(payload,dict) else []
    if isinstance(messages,dict): messages=[messages]
    for item in messages: process_telemetry(normalize(item))
    return {'ok':True,'processed':len(messages)}
@app.post('/admin/set-telegram-webhook/{secret}')
def admin_set_telegram_webhook(secret:str):
    if secret!=settings.webhook_secret: raise HTTPException(status_code=403,detail='Invalid admin secret')
    return set_webhook()
@app.post('/admin/delete-telegram-webhook/{secret}')
def admin_delete_telegram_webhook(secret:str):
    if secret!=settings.webhook_secret: raise HTTPException(status_code=403,detail='Invalid admin secret')
    return delete_webhook()
@app.post('/admin/test-message/{secret}')
def admin_test_message(secret:str):
    if secret!=settings.webhook_secret: raise HTTPException(status_code=403,detail='Invalid admin secret')
    return send_message('✅ Teltonika Flespi Telegram Bot test message.',disable_web_page_preview=True)
