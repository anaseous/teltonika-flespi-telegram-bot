import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
@dataclass
class Settings:
    app_public_url: str = os.getenv('APP_PUBLIC_URL','')
    webhook_secret: str = os.getenv('WEBHOOK_SECRET','change-me')
    telegram_bot_token: str = os.getenv('TELEGRAM_BOT_TOKEN','')
    telegram_chat_id: str = os.getenv('TELEGRAM_CHAT_ID','')
    flespi_token: str = os.getenv('FLESPI_TOKEN','')
    flespi_device_id: str = os.getenv('FLESPI_DEVICE_ID','')
    timezone: str = os.getenv('TIMEZONE','Asia/Dubai')
    location_interval_sec: int = int(os.getenv('LOCATION_INTERVAL_SEC','300'))
    daily_report_time: str = os.getenv('DAILY_REPORT_TIME','00:00')
    idle_speed_kmh: float = float(os.getenv('IDLE_SPEED_KMH','3'))
    trip_min_duration_sec: int = int(os.getenv('TRIP_MIN_DURATION_SEC','60'))
    device_name: str = os.getenv('DEVICE_NAME','Teltonika FMC920/FMB920')
    sqlite_path: str = os.getenv('SQLITE_PATH','data/bot.sqlite')
settings = Settings()
