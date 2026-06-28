# Flespi Telegram Channel

Flespi has a Telegram protocol that acts as a Telegram bot gateway.

This allows Flespi to:

- receive text messages from Telegram users
- receive location messages from Telegram users
- parse Telegram messages into normalized parameters
- send text messages back to Telegram users

Recommended use:

```text
Telegram user command → Flespi Telegram Channel → Flespi REST/API action → Telegram reply
```

Example Telegram commands:

```text
/status
/location
/interval 5min
/daily 00:00
/report yesterday
```
