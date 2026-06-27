# Teltonika Flespi Telegram Bot for FMC920 and FMB920

A ready-to-deploy **Teltonika + Flespi + Telegram only** solution for FMC920 and FMB920 trackers. The Teltonika device sends GPS data to a Flespi Teltonika channel using TCP or MQTT, and this bot receives normalized Flespi telemetry then sends Telegram alerts with Google Maps location, OpenStreetMap live tracking link, ignition status, towing alerts, and automatic daily reports at 12:00 AM for previous-day idling time, average trip time, and number of trips.

**SEO keywords:** Teltonika Telegram bot, FMB920 Telegram alerts, FMC920 Telegram tracking, Flespi Telegram integration, Teltonika Flespi MQTT, Teltonika TCP tracking, Google Maps Telegram GPS, OpenStreetMap live tracking, Teltonika towing alert, Teltonika idling report, fleet tracking Telegram bot.

---

## What this project does

- Receives Teltonika FMC920 / FMB920 telemetry through Flespi MQTT.
- Sends Telegram location messages with Google Maps and OpenStreetMap links.
- Sends ignition status updates.
- Sends towing alert immediately.
- Calculates idling time from ignition ON and low-speed records.
- Calculates trip count from ignition ON/OFF transitions.
- Sends previous-day daily report every day at 12:00 AM.
- Runs using Docker on Linux, VPS, mini PC, or Raspberry Pi.

## Important architecture

Do **not** point the Teltonika tracker directly to Telegram. Use this flow:

```text
Teltonika FMC920 / FMB920 -> Flespi Teltonika Channel -> This Bot -> Telegram
```

## Sample Teltonika server URL and port

Example only:

```text
Domain: abc123.flespi.gw
Port: 21543
Protocol: TCP
```

Copy your real domain and port from your Flespi channel.

## Deploy today - non-technical steps

### 1. Create Telegram bot

Open Telegram, search `BotFather`, send `/newbot`, follow instructions, copy the bot token, then open your bot and press **Start**.

### 2. Get Telegram chat ID

Send any message to your bot, then open:

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

Find and copy:

```json
"chat":{"id":123456789}
```

### 3. Create Flespi Teltonika channel

Create a Flespi account, create a Teltonika channel, copy the domain and port, add your FMC920/FMB920 IMEI as a device, then confirm data in Logs & Messages.

### 4. Configure Teltonika FMC920 / FMB920

Open Teltonika Configurator -> GPRS settings -> enter SIM APN -> First Server Settings -> enter Flespi domain and port -> Protocol TCP -> Save to device -> Reboot tracker.

### 5. Run this bot

```bash
git clone https://github.com/YOUR-USERNAME/teltonika-flespi-telegram-bot.git
cd teltonika-flespi-telegram-bot
cp .env.example .env
```

Edit `.env`:

```env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
FLESPI_TOKEN=YOUR_FLESPI_TOKEN
TIMEZONE=Asia/Dubai
DAILY_REPORT_TIME=00:00
DEVICE_NAME=Teltonika FMC920/FMB920
```

Start:

```bash
docker compose up -d --build
```

Check logs:

```bash
docker logs -f teltonika-flespi-telegram-bot
```

## Test without real tracker

Set this in `.env`:

```env
RUN_SAMPLE_ON_START=true
```

Run:

```bash
docker compose up --build
```


---

## Telegram user commands - select time intervals from Telegram

The end user can change reporting intervals directly from Telegram without editing the server. Send these commands to the bot:

```text
/help
/settings
/interval 5min
/interval 15min
/interval 30min
/interval 1h
/interval off
/daily 00:00
```

Examples:

```text
/interval 10min
```

This sends Google Maps and OpenStreetMap location updates every 10 minutes.

```text
/daily 23:30
```

This changes the daily previous-day summary report time to 23:30 using the timezone configured in `.env`.

The bot accepts commands only from the configured `TELEGRAM_CHAT_ID`.

## Production recommendations

- Keep `.env` private.
- Keep the Flespi token private.
- Use Docker restart policy.
- Enable correct I/O parameters in Teltonika Configurator.
- Verify ignition and towing parameter names in Flespi messages.
- Keep `LOCATION_SEND_INTERVAL_SEC` at 300 seconds or more to avoid Telegram spam.

## Repository structure

```text
teltonika-flespi-telegram-bot/
├── app/
├── docs/
├── samples/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── PROJECT_DESCRIPTION.md
└── README.md
```

## License

MIT License.
