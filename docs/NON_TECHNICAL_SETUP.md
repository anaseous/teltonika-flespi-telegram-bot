# Non-Technical Setup Guide

This solution does not use Docker, webhooks, domains, public IP, or port forwarding.

The flow is:

```text
Teltonika FMC920/FMB920 -> Flespi -> Python polling bot -> Telegram
```

The Python bot can run on a normal Windows PC, Linux PC, laptop, mini PC, or Raspberry Pi. The device still sends data to Flespi. The bot reads Flespi using REST API and reads Telegram commands using long polling.

## Step 1 - Create Telegram Bot

1. Open Telegram.
2. Search for `BotFather`.
3. Send `/newbot`.
4. Copy the token.
5. Open your new bot and press Start.
6. Send any message to the bot.
7. Open:

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

8. Copy `chat.id`.

## Step 2 - Create Flespi Teltonika Channel

1. Log in to Flespi.
2. Create a Teltonika channel.
3. Copy the channel domain and port.
4. Create a Flespi device using the FMC920/FMB920 IMEI.
5. Copy the Flespi Device ID.
6. Confirm data appears in Flespi messages.

## Step 3 - Configure Teltonika Configurator

Use your Flespi channel values:

```text
Domain: abc123.flespi.gw
Port: 21543
Protocol: TCP
```

Save to device and reboot the tracker.

## Step 4 - Install the bot on Windows

Double-click `scripts/install_windows.bat`, edit `.env`, then double-click `scripts/run_windows.bat`.

## Step 5 - Use Telegram Commands

```text
/help
/status
/location
/settings
/interval 5min
/interval 1h
/interval off
/daily 00:00
/report yesterday
```
