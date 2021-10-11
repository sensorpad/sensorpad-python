# sensorpad-python

Sensorpad-python is a library for sending events to Sensorpad.

This library does not install dependencies, so you don't have to worry about Requests package version compatibility.


## Installation

You need python3 to use this library.

```
pip install sensorpad --upgrade
```

## Base usage

```python
from sensorpad import Event

event = Event('b24e4093-db36-4b5c-8c7a-16...')

event.send(value=1)
```

That's it.

```python
event.__dict__
```

Shows the state of current event

```python
{'sensor_code': 'b24e4093-db36-4b5c-8c7a-16...',
 'id': 116184,
 'status': 'complete',
 'value': '1',
 'sensor_name': 'Test sensor',
 'started': datetime.datetime(2021, 9, 28, 0, 52, 26, 625234, tzinfo=tzutc()),
 'completed': datetime.datetime(2021, 9, 28, 0, 52, 26, 626234, tzinfo=tzutc()),
 'next_scheduled_run': '2021-09-25T13:20:00Z',
 'duration': 0.001,
 'delay': 285.814256,
 'interval_between_starts': 59.986451,
 'interval_between_completes': 43415.197581,
 'endpoint': 'https://sensorpad.link/'}
```


## Advanced usage

### Measuring time of event

```python
import time
from sensorpad import Event

event = Event('b24e4093-db36-4b5c-8c7a-16...')

event.start()
time.sleep(5)
event.complete(value=42)
```

This way affects event `duration`:

```python
{'sensor_code': 'b24e4093-db36-4b5c-8c7a-16...',
 'id': 118178,
 'status': 'complete',
 'value': '42',
 ...
 'started': datetime.datetime(2021, 9, 28, 0, 49, 6, 972973, tzinfo=tzutc()),
 'completed': datetime.datetime(2021, 9, 28, 0, 49, 12, 522658, tzinfo=tzutc()),
 'duration': 5.549685,
 ...}
```

## Wanna use Sensorpad via plain API?

Please check the documentation: 

https://sensorpad.io/docs/simple-events/
