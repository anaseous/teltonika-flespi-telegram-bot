import os, requests
from dotenv import load_dotenv
load_dotenv()
TOKEN=os.getenv('TELEGRAM_BOT_TOKEN'); PUBLIC_URL=os.getenv('APP_PUBLIC_URL','').rstrip('/'); SECRET=os.getenv('WEBHOOK_SECRET')
r=requests.post(f'https://api.telegram.org/bot{TOKEN}/setWebhook',json={'url':f'{PUBLIC_URL}/telegram/{SECRET}','drop_pending_updates':True},timeout=20)
print(r.status_code); print(r.text)
