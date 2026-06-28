import requests
from .config import settings
BASE='https://flespi.io'
def headers(): return {'Authorization':f'FlespiToken {settings.flespi_token}','Content-Type':'application/json'}
def get_latest_messages(limit=100):
    if not settings.flespi_device_id: return []
    r=requests.get(f'{BASE}/gw/devices/{settings.flespi_device_id}/messages',headers=headers(),params={'limit':limit,'reverse':'true'},timeout=30)
    r.raise_for_status(); data=r.json(); result=data.get('result',[]) if isinstance(data,dict) else data
    return list(reversed(result))
