import datetime
import json

from sensorpad.constants import COMPLETE_STATUS, START_STATUS
from sensorpad.helpers.exceptions import (EventAlreadyComplete,
                                          EventAlreadyStarted)
from sensorpad.helpers.parsers import isoformat_parser
from sensorpad.helpers.simple_requests import request
from sensorpad.settings import API_ENDPOINT


class Event(object):
    """Sensorpad event."""

    def __init__(self, sensor_code, api_endpoint=API_ENDPOINT):
        self.sensor_code = sensor_code
        self.id = None
        self.satus = None
        self.value = None
        self.sensor_name = None
        self.started = None
        self.completed = None
        self.next_scheduled_run = None
        self.duration = None
        self.delay = None
        self.next_scheduled_run = None
        self.interval_between_starts = None
        self.interval_between_completes = None
        self.endpoint = api_endpoint
        # check if someone pass entire url as code
        if '/' in self.sensor_code:
            self.sensor_code = self.sensor_code.split('/')[-1]

    def __repr__(self):
        """Text representation."""

        def json_datetime_serializer(o):
            if isinstance(o, (datetime.date, datetime.datetime)):
                return o.isoformat()

        return json.dumps(self.__dict__, default=json_datetime_serializer)

    def _sensor_request(self, request_url, params=None):
        """Request to sensor."""
        response = request(request_url, params=params)
        if response.status_code == 200:
            self.update_from_dict(response.json())
        if response.status_code == 417:
            raise EventAlreadyComplete()
        # TO DO: different exceptions on different status codes
        else:
            err = 'Sensor returned status code {code} and response: {content}'
            raise RuntimeError(
                err.format(
                    code=response.status_code, content=response.text
                )
            )

    def update_from_dict(self, event_as_dict):
        """Make or update event from dict."""
        self.id = event_as_dict.get('event_id')
        self.status = event_as_dict.get('status')
        self.value = event_as_dict.get('value')
        self.sensor_code = event_as_dict.get('sensor')
        self.sensor_name = event_as_dict.get('name')
        self.started = isoformat_parser(event_as_dict.get('started'))
        self.completed = isoformat_parser(event_as_dict.get('completed'))
        self.next_scheduled_run = isoformat_parser(
            event_as_dict.get('next_scheduled_run')
        )
        self.duration = event_as_dict.get('duration')
        self.delay = event_as_dict.get('delay')
        self.next_scheduled_run = event_as_dict.get('next_scheduled_run')
        self.interval_between_starts = event_as_dict.get(
            'interval_between_starts'
        )
        self.interval_between_completes = event_as_dict.get(
            'interval_between_completes'
        )

    def start(self, value=None):
        """Start Sensorpad event."""
        if self.status == START_STATUS:
            raise EventAlreadyStarted(self.id)
        if self.status == COMPLETE_STATUS:
            raise EventAlreadyComplete(self.id)
        request_url = '{endpoint}{code}/start'.format(
            endpoint=self.endpoint, code=self.sensor_code
        )
        params = {}
        if value:
            params['value'] = value

        self._sensor_request(request_url, params=params)

    def complete(self, value=None):
        """Complete Sensorpad event."""
        if self.status == COMPLETE_STATUS:
            raise EventAlreadyComplete(self.id)
        if not self.id:
            request_url = '{endpoint}{code}/'.format(
                endpoint=self.endpoint,
                code=self.sensor_code
            )
        else:
            request_url = '{endpoint}{code}/complete/{event_id}/'.format(
                endpoint=self.endpoint,
                code=self.sensor_code,
                event_id=self.id
            )
        params = {}
        if value:
            params['value'] = value

        return self._sensor_request(request_url, params=params)

    def send(self, value=None):
        """Start and complete event. This is alias for `complete`."""
        self.complete(value=value)
