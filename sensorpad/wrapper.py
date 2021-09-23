from sensorpad.helpers.simple_requests import request
from sensorpad.settings import API_ENDPOINT


class Event(object):
    """Sensorpad event."""

    def __init__(self, response=None):
        if response:
            self.from_dict(response)

    def from_dict(self, event_as_dict):
        """Make event from dict."""
        pass


class Sensor(object):
    """Sensor operations."""

    def __init__(self, sensor_code, api_endpoint=API_ENDPOINT):
        self.code = sensor_code
        self.endpoint = api_endpoint
        # check if someone pass entire url as code
        if '/' in self.code:
            self.code = self.code.split('/')[-1]

    def __repr__(self):
        """Text representation."""
        return 'Sensor with code: `{code}`'.format(code=self.code)

    def _sensor_request(self, request_url, params=None):
        """Request to sensor."""
        response = request(request_url, params=params)
        if response.status_code == 200:
            event = Event(response=response.json())
            return event
        # TO DO: different exceptions on different status codes
        else:
            err = 'Sensor returned status code {code} and response: {content}'
            raise RuntimeError(
                err.format(
                    code=response.status_code, content=response.text
                )
            )

    def start_event(self, value=None):
        """Start Sensorpad event."""
        request_url = '{endpoint}{code}/start'.format(
            endpoint=self.endpoint, code=self.code
        )
        params = {}
        if value:
            params['value'] = value

        return self._sensor_request(request_url, params=params)

    def complete_event(self, value=None, event_id=None):
        """Complete Sensorpad event."""
        if not event_id:
            request_url = '{endpoint}{code}/'.format(
                endpoint=self.endpoint, code=self.code
            )
        else:
            request_url = '{endpoint}{code}/complete/{event_id}/'.format(
                endpoint=self.endpoint, code=self.code, event_id=event_id
            )
        params = {}
        if value:
            params['value'] = value

        return self._sensor_request(request_url, params=params)

    def send_event(self, value=None, event_id=None):
        """Start and complete event. This is alias for `complete_event`."""
        self.complete_event(value=value, event_id=event_id)
