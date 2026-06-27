import json, ssl, time, threading
from pathlib import Path
import paho.mqtt.client as mqtt
from .config import settings
from .storage import init_db
from .normalizer import normalize_message
from .processor import process_telemetry
from .daily import maybe_send_daily_report
from .telegram import send_telegram
from .bot_commands import polling_loop

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected to Flespi MQTT: {reason_code}")
    client.subscribe(settings.flespi_mqtt_topic, qos=1)
    print(f"Subscribed to: {settings.flespi_mqtt_topic}")

def on_message(client, userdata, msg):
    try:
        payload=json.loads(msg.payload.decode("utf-8", errors="ignore"))
        if isinstance(payload, list):
            for item in payload: process_telemetry(normalize_message(item, msg.topic))
        else: process_telemetry(normalize_message(payload, msg.topic))
    except Exception as exc: print(f"Failed to process MQTT message from {msg.topic}: {exc}")

def daily_loop():
    while True:
        try: maybe_send_daily_report()
        except Exception as exc: print(f"Daily report error: {exc}")
        time.sleep(30)

def run_sample_once():
    sample=Path("samples/sample_flespi_messages.json")
    for item in json.loads(sample.read_text(encoding="utf-8")): process_telemetry(normalize_message(item,"sample"))
    print("Sample processing completed.")

def main():
    init_db()
    if settings.run_sample_on_start: run_sample_once(); return
    threading.Thread(target=daily_loop, daemon=True).start()
    threading.Thread(target=polling_loop, daemon=True).start()
    client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="teltonika-flespi-telegram-bot")
    client.username_pw_set(settings.flespi_token, "")
    if settings.flespi_mqtt_port == 8883: client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    client.on_connect=on_connect; client.on_message=on_message
    print(f"Connecting to Flespi MQTT {settings.flespi_mqtt_host}:{settings.flespi_mqtt_port} ...")
    client.connect(settings.flespi_mqtt_host, settings.flespi_mqtt_port, keepalive=60)
    try: send_telegram("✅ Teltonika Flespi Telegram Bot started.", disable_web_page_preview=True)
    except Exception as exc: print(f"Telegram startup message failed: {exc}")
    client.loop_forever()
if __name__ == "__main__": main()
