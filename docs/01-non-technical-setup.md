# Non-Technical Setup Guide

## Goal

Use only:

```text
Teltonika FMC920/FMB920
Flespi
Telegram
```

No other system is required.

---

## Step 1 — Create Telegram Bot

1. Open Telegram.
2. Search for `BotFather`.
3. Send `/newbot`.
4. Copy the bot token.
5. Send a message to the bot.
6. Keep the bot token safe.

---

## Step 2 — Create Flespi Teltonika Channel

1. Log in to Flespi.
2. Open **Telematics Hub**.
3. Create a new **Teltonika** channel.
4. Copy the channel domain and port.
5. Create a Flespi device using the FMC920/FMB920 IMEI.
6. Confirm device messages appear in Flespi.

Example only:

```text
Domain: abc123.flespi.gw
Port: 21543
Protocol: TCP
```

---

## Step 3 — Configure Teltonika Configurator

In Teltonika Configurator:

```text
GPRS → Server Settings
Domain: Flespi channel domain
Port: Flespi channel port
Protocol: TCP
```

Save to device and reboot tracker.

---

## Step 4 — Create Flespi Telegram Channel

1. In Flespi, create a channel using the **Telegram** protocol.
2. Connect the Telegram Bot token.
3. Send a message from Telegram to the bot.
4. Confirm Flespi receives Telegram text messages.

---

## Step 5 — Configure Telegram Command Actions in Flespi

Create Flespi-side actions for:

```text
/status
/location
/interval 5min
/interval 15min
/interval 1h
/daily 00:00
/report yesterday
```

The actions update Flespi configuration and send Telegram replies.

---

## Step 6 — Test

Open Telegram and send:

```text
/status
/location
/interval 5min
```

Expected result:

- Flespi returns latest location.
- Telegram receives Google Maps and OpenStreetMap links.
- Flespi updates the configured reporting interval.
