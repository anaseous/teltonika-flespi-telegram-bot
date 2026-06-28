# Non-Technical Setup Guide

Flow:

```text
Teltonika FMC920/FMB920 -> Flespi -> Telegram Bot -> Flespi REST API
```

## 1. Create Telegram bot

Open Telegram, search `BotFather`, send `/newbot`, copy the token, open the bot and press Start. Send any message to the bot, then open:

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

Copy `chat.id`.

## 2. Create Flespi Teltonika channel

Create a Flespi Teltonika channel, copy the channel domain and port, add your FMC920/FMB920 IMEI as a device, and confirm messages appear in Logs & Messages.

## 3. Configure Teltonika Configurator

```text
GPRS -> First Server Settings
Domain: your Flespi channel domain
Port: your Flespi channel port
Protocol: TCP
```

Example only:

```text
Domain: abc123.flespi.gw
Port: 21543
Protocol: TCP
```

## 4. Deploy this bot

Deploy the Docker app to an always-on HTTPS public URL. After deployment, your local PC is no longer needed.

## 5. Register Telegram webhook

Open:

```text
https://YOUR_PUBLIC_URL/admin/set-telegram-webhook/YOUR_WEBHOOK_SECRET
```

## 6. Configure Flespi webhook

Send normalized Flespi messages to:

```text
https://YOUR_PUBLIC_URL/flespi/YOUR_WEBHOOK_SECRET
```

## 7. Use Telegram commands

```text
/help
/status
/location
/interval 5min
/interval 1h
/interval off
/daily 00:00
/report yesterday
```
