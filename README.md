# sensorpad-python

Sensorpad-python is a library for sending events to Sensorpad.

This library does not install dependencies, so you don't have to worry about Requests package version compatibility.


## Base usage

```
from sensorpad import Event

event = Event('b24e4093-db36-4b5c-8c7a-16...')

event.send(value=1)
```

That's it.

```event.__dict__```

Shows the state of current event

```
{'sensor_code': 'b24e4093-db36-4b5c-8c7a-16...',
 'id': 116184,
 'status': 'complete',
 'value': 1,
 'sensor_name': 'Test sensor',
 'started': datetime.datetime(2021, 9, 25, 13, 18, 22, 686396, tzinfo=tzutc()),
 'completed': datetime.datetime(2021, 9, 25, 13, 24, 45, 814256, tzinfo=tzutc()),
 'next_scheduled_run': '2021-09-25T13:20:00Z',
 'duration': 383.12786,
 'delay': 285.814256,
 'interval_between_starts': 59.986451,
 'interval_between_completes': 43415.197581,
 'endpoint': 'https://sensorpad.link/'}
```