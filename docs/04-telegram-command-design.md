# Telegram Command Design

## User Commands

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

## Command Logic

### /status

Flespi reads latest device telemetry and replies with:

```text
Ignition
Speed
Last update time
Fuel/voltage if available
```

### /location

Flespi replies with:

```text
Google Maps link
OpenStreetMap link
```

### /interval 5min

Flespi updates the reporting interval stored in Flespi configuration.

### /daily 00:00

Flespi updates the daily report schedule.

### /report yesterday

Flespi sends previous-day statistics.
