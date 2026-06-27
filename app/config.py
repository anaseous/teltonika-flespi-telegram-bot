import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
@dataclass
class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    flespi_mqtt_host: str = os.getenv("FLESPI_MQTT_HOST", "mqtt.flespi.io")
    flespi_mqtt_port: int = int(os.getenv("FLESPI_MQTT_PORT", "8883"))
    flespi_token: str = os.getenv("FLESPI_TOKEN", "")
    flespi_mqtt_topic: str = os.getenv("FLESPI_MQTT_TOPIC", "flespi/message/gw/devices/+/telemetry/+")
    timezone: str = os.getenv("TIMEZONE", "Asia/Dubai")
    daily_report_time: str = os.getenv("DAILY_REPORT_TIME", "00:00")
    send_location_on_every_message: bool = os.getenv("SEND_LOCATION_ON_EVERY_MESSAGE", "false").lower() == "true"
    location_send_interval_sec: int = int(os.getenv("LOCATION_SEND_INTERVAL_SEC", "300"))
    send_ignition_change: bool = os.getenv("SEND_IGNITION_CHANGE", "true").lower() == "true"
    send_towing_alert: bool = os.getenv("SEND_TOWING_ALERT", "true").lower() == "true"
    idle_speed_kmh: float = float(os.getenv("IDLE_SPEED_KMH", "3"))
    trip_min_duration_sec: int = int(os.getenv("TRIP_MIN_DURATION_SEC", "60"))
    device_name: str = os.getenv("DEVICE_NAME", "Teltonika FMC920/FMB920")
    sqlite_path: str = os.getenv("SQLITE_PATH", "data/teltonika_bot.sqlite")
    run_sample_on_start: bool = os.getenv("RUN_SAMPLE_ON_START", "false").lower() == "true"
settings = Settings()
