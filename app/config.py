import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
@dataclass
class Settings:
    telegram_bot_token: str = os.getenv('TELEGRAM_BOT_TOKEN','')
    telegram_chat_id: str = os.getenv('TELEGRAM_CHAT_ID','')
    flespi_token: str = os.getenv('FLESPI_TOKEN','')
    flespi_device_id: str = os.getenv('FLESPI_DEVICE_ID','')
    timezone: str = os.getenv('TIMEZONE','Asia/Dubai')
    flespi_poll_interval_sec: int = int(os.getenv('FLESPI_POLL_INTERVAL_SEC','30'))
    telegram_poll_timeout_sec: int = int(os.getenv('TELEGRAM_POLL_TIMEOUT_SEC','30'))
    location_interval_sec: int = int(os.getenv('LOCATION_INTERVAL_SEC','300'))
    daily_report_time: str = os.getenv('DAILY_REPORT_TIME','00:00')
    idle_speed_kmh: float = float(os.getenv('IDLE_SPEED_KMH','3'))
    trip_min_duration_sec: int = int(os.getenv('TRIP_MIN_DURATION_SEC','60'))
    device_name: str = os.getenv('DEVICE_NAME','Teltonika FMC920/FMB920')
    sqlite_path: str = os.getenv('SQLITE_PATH','data/bot.sqlite')
settings=Settings()
