# Teltonika Flespi Telegram Bot for FMC920 and FMB920

A production-ready **no-webhook, no-domain, no-Docker** Teltonika + Flespi + Telegram solution for FMC920 and FMB920 trackers. Teltonika sends GPS data to Flespi. This lightweight Python bot reads Flespi through REST API and uses Telegram long polling to receive user commands and send Google Maps location, OpenStreetMap live tracking links, ignition updates, towing alerts, and daily reports.

**SEO keywords:** Teltonika Telegram bot, FMB920 Telegram alerts, FMC920 Telegram tracking, Flespi Telegram integration, Teltonika Flespi REST API, no webhook Telegram bot, no Docker GPS tracking, Google Maps Telegram GPS, OpenStreetMap live tracking, Teltonika towing alert, Teltonika idling report.

---

## Architecture

```text
Teltonika FMC920/FMB920
        ↓ TCP
      Flespi
        ↓ REST API polling
 Python Telegram Bot
        ↓ Telegram Bot API long polling
      Telegram
```

No public domain, no static IP, no webhook, no port forwarding, and no Docker are required.

> The PC or Raspberry Pi running this bot must stay powered on because the bot performs Telegram long polling and Flespi REST polling.

---

## Features

- Dedicated for Teltonika FMC920/FMB920.
- Works with Flespi only as middleware.
- Google Maps location link.
- OpenStreetMap live tracking link.
- Ignition status update.
- Towing alert.
- Daily previous-day report at 12:00 AM.
- Idling time calculation.
- Average trip time calculation.
- Number of trips calculation.
- Telegram commands for non-technical users.

---

## Telegram Commands

```text
/help
/status
/location
/settings
/interval 5min
/interval 15min
/interval 30min
/interval 1h
/interval off
/daily 00:00
/report yesterday
/report today
```

---

## Sample Teltonika Configurator Server Settings

```text
Domain: abc123.flespi.gw
Port: 21543
Protocol: TCP
```

---

## Windows Setup for Non-Technical Users

1. Download this repository ZIP from GitHub and extract it.
2. Install Python 3.11 or newer from `https://www.python.org/downloads/` and tick `Add Python to PATH`.
3. Double-click `scripts/install_windows.bat`.
4. Edit `.env` in Notepad and add Telegram/Flespi details.
5. Double-click `scripts/run_windows.bat` and keep the window open.

Required `.env` values:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
FLESPI_TOKEN=your_flespi_token
FLESPI_DEVICE_ID=your_flespi_device_id
TIMEZONE=Asia/Dubai
LOCATION_INTERVAL_SEC=300
DAILY_REPORT_TIME=00:00
```

---

## Linux / Raspberry Pi Setup

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
chmod +x scripts/install_linux.sh scripts/run_linux.sh
./scripts/install_linux.sh
nano .env
./scripts/run_linux.sh
```

---

## Confirm It Works

Send these Telegram commands:

```text
/help
/status
/location
/interval 5min
```

---

## Important Notes

- No domain is needed because Telegram long polling is used.
- No webhook is needed because the bot continuously asks Telegram for new messages.
- No Docker is needed.
- One always-on PC, mini PC, Linux machine, or Raspberry Pi is still required to run the Python script.
- Do not upload `.env` to GitHub.

---

## Repository Structure

```text
teltonika-flespi-telegram-bot/
├── app/
├── docs/
├── scripts/
├── samples/
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## License

MIT License.
