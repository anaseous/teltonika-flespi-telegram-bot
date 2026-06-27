# Teltonika FMC920 / FMB920 Setup Guide

## Important correction
A Teltonika tracker cannot send TCP AVL packets directly to a Telegram Bot API URL. Telegram Bot API is used by this bot to send messages to Telegram. The tracker must point to your Flespi Teltonika channel host and port.

## Sample server URL and port
Use your real Flespi channel domain and port from Flespi.

Example only:

```text
Domain: abc123.flespi.gw
Port: 21543
Protocol: TCP
```

## Teltonika Configurator steps

1. Connect FMC920 or FMB920 to your PC using USB.
2. Open Teltonika Configurator.
3. Open the device.
4. Go to GPRS settings.
5. Enter SIM APN details.
6. Go to First Server Settings.
7. Set Domain to your Flespi channel domain.
8. Set Port to your Flespi channel port.
9. Set Protocol to TCP.
10. Save to device.
11. Reboot the tracker.
12. Confirm data in Flespi Channel Logs & Messages.

## Recommended I/O parameters
Enable GNSS location, speed, ignition status, towing event, movement status, external voltage, battery voltage, and trip/odometer if available.

## MQTT option
If your FMC920/FMB920 firmware supports Teltonika MQTT, create a Flespi Teltonika Mobility MQTT channel and use that channel host and port in MQTT settings.
