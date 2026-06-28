# Teltonika Flespi Telegram Bot for FMC920 and FMB920

A production-ready **Teltonika + Flespi + Telegram** solution for FMC920 and FMB920 trackers. Teltonika sends GPS data to a Flespi Teltonika channel. Flespi forwards normalized telemetry to this bot. Telegram users receive Google Maps location links, OpenStreetMap live tracking links, ignition updates, towing alerts, and daily reports. Telegram commands can also query Flespi REST API and change reporting intervals without touching the server.

**SEO keywords:** Teltonika Telegram bot, FMB920 Telegram alerts, FMC920 Telegram tracking, Flespi Telegram integration, Teltonika Flespi REST API, Teltonika TCP tracking, Google Maps Telegram GPS, OpenStreetMap live tracking, Teltonika towing alert, Teltonika idling report, fleet tracking Telegram bot.

---

## Architecture

```text
Teltonika FMC920/FMB920
        ↓ TCP or MQTT
      Flespi
        ↓ Webhook / normalized telemetry
 Telegram Bot Service
        ↓ Flespi REST API
      Telegram
```

The Teltonika device does not point directly to Telegram. It points to the Flespi channel domain and port.

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

Example only:

```text
Domain: abc123.flespi.gw
Port: 21543
Protocol: TCP
```

---

## Deploy Today

```bash
cp .env.example .env
docker compose up -d --build
```

Edit `.env` before starting:

```env
APP_PUBLIC_URL=https://your-public-domain.com
WEBHOOK_SECRET=change-this-long-random-secret
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
FLESPI_TOKEN=your_flespi_token
FLESPI_DEVICE_ID=your_flespi_device_id
TIMEZONE=Asia/Dubai
LOCATION_INTERVAL_SEC=300
DAILY_REPORT_TIME=00:00
```

Register Telegram webhook:

```text
https://YOUR_PUBLIC_URL/admin/set-telegram-webhook/YOUR_WEBHOOK_SECRET
```

Configure Flespi webhook:

```text
https://YOUR_PUBLIC_URL/flespi/YOUR_WEBHOOK_SECRET
```

Configure Teltonika FMC920/FMB920 in Teltonika Configurator:

```text
GPRS -> First Server Settings
Domain: Flespi channel domain
Port: Flespi channel port
Protocol: TCP
```

After deployment, no local PC is required.

---

## Repository Structure

```text
teltonika-flespi-telegram-bot/
├── app/
├── docs/
├── scripts/
├── samples/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Security Notes

- Never commit `.env` to GitHub.
- Keep `FLESPI_TOKEN` private.
- Keep `TELEGRAM_BOT_TOKEN` private.
- Use HTTPS for the public URL.
- Restrict the Telegram bot to your configured `TELEGRAM_CHAT_ID`.
