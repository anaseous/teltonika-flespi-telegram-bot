# Teltonika FMC920/FMB920 → Flespi → Telegram Bot

**Teltonika + Flespi + Telegram** configuration blueprint. No Python app, no Docker, no Raspberry Pi, no VPS, no domain, no custom webhook server, and no external middleware.

The tracker sends data to **Flespi**. Flespi parses Teltonika telemetry, calculates events/reports, sends messages to **Telegram**, receives Telegram commands using a Flespi Telegram channel, and updates Flespi configuration using Flespi REST API.

---

## Architecture

```text
Teltonika FMC920/FMB920
        ↓ TCP to Flespi Teltonika Channel
      Flespi
        ├─ device telemetry
        ├─ calculators / intervals / reports
        ├─ Flespi Telegram Channel receives commands
        ├─ Flespi REST API updates settings
        ↓
 Telegram Bot
```

There is no locally running bot. Telegram is only the chat interface. Flespi is the automation brain.

---

## What Telegram Can Do

Telegram user sends:

```text
/status
/location
/interval 5min
/interval 15min
/interval 1h
/daily 00:00
/report yesterday
```

Flespi receives the Telegram text message through the **Flespi Telegram protocol channel**, interprets it through Flespi-side automation, updates Flespi configuration using REST API, and replies back to the Telegram user.

---

## What Flespi Sends to Telegram

- Google Maps location link
- OpenStreetMap live tracking link
- Ignition status
- Towing alert
- Daily previous-day idling time
- Daily previous-day average trip time
- Daily previous-day number of trips
- User-selected location interval updates

---

## Repository Contents

```text
teltonika-flespi-telegram-bot/
├── README.md
├── PROJECT_DESCRIPTION.md
├── docs/
│   ├── 01-non-technical-setup.md
│   ├── 02-flespi-telegram-channel.md
│   ├── 03-teltonika-fmc920-fmb920-setup.md
│   ├── 04-telegram-command-design.md
│   └── 05-production-checklist.md
└── templates/
    ├── telegram-message-templates.json
    ├── telegram-command-mapping.json
    └── flespi-rest-api-actions.json
```

---

## SEO Keywords

Teltonika Telegram bot, FMC920 Telegram tracking, FMB920 Telegram alerts, Flespi Telegram integration, Teltonika Flespi REST API, Flespi Telegram protocol, Google Maps Telegram GPS, OpenStreetMap live tracking, Teltonika towing alert, Teltonika idling report, no Docker GPS tracking, no webhook Telegram GPS.
