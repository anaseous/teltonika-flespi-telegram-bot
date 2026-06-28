# Flespi Webhook Setup

Create a Flespi webhook/stream that forwards normalized messages to:

```text
https://YOUR_PUBLIC_URL/flespi/YOUR_WEBHOOK_SECRET
```

Accepted fields include:

```text
position.latitude
position.longitude
position.speed
engine.ignition.status
towing.event
device.id
ident
timestamp
```
