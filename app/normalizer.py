import json, time

def pick(data, *keys, default=None):
    for k in keys:
        if k in data and data[k] is not None:
            return data[k]
    return default

def normalize_message(payload: dict, topic: str = ""):
    data = payload if isinstance(payload, dict) else {}
    device_id = str(pick(data, "device.id", "device_id", "ident", "imei", default="unknown"))
    ts = int(pick(data, "timestamp", "server.timestamp", "time", default=time.time()))
    lat = pick(data, "position.latitude", "lat", "latitude")
    lon = pick(data, "position.longitude", "lon", "lng", "longitude")
    speed = float(pick(data, "position.speed", "speed", "vehicle.speed", default=0) or 0)
    ignition = bool(pick(data, "engine.ignition.status", "ignition", "ignition.status", default=False))
    towing_raw = pick(data, "towing.event", "towing.status", "alarm.event", "event.enum", default=False)
    towing = str(towing_raw).lower() in ["true", "1", "towing", "tow", "towing_detected"] or towing_raw is True
    return {"device_id": device_id, "ts": ts, "lat": float(lat) if lat is not None else None, "lon": float(lon) if lon is not None else None, "speed": speed, "ignition": ignition, "towing": towing, "raw": json.dumps(payload, ensure_ascii=False)}
