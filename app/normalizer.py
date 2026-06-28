import json,time
def pick(d,*keys,default=None):
    for k in keys:
        if isinstance(d,dict) and k in d and d[k] is not None: return d[k]
    return default
def normalize(payload):
    d=payload if isinstance(payload,dict) else {}
    tow=pick(d,'towing.event','towing.status','alarm.event','event.enum',default=False)
    return {'device_id':str(pick(d,'device.id','device_id','ident','imei',default='unknown')),'ts':int(pick(d,'timestamp','server.timestamp','time',default=time.time())),'lat':float(pick(d,'position.latitude','lat','latitude')) if pick(d,'position.latitude','lat','latitude') is not None else None,'lon':float(pick(d,'position.longitude','lon','lng','longitude')) if pick(d,'position.longitude','lon','lng','longitude') is not None else None,'speed':float(pick(d,'position.speed','speed','vehicle.speed',default=0) or 0),'ignition':bool(pick(d,'engine.ignition.status','ignition','ignition.status',default=False)),'towing':tow is True or str(tow).lower() in ['true','1','tow','towing','towing_detected'],'raw':json.dumps(payload,ensure_ascii=False)}
