class EventAlreadyStarted(RuntimeError):
    """Raise when event is already started."""
    def __init__(self, event_id):
        self.message = """
            Event is already STARTED and has ID: {0},
            you need complete current event
            or instantiate new object of this class
            to send new event.""".format(event_id)
        try:
            super(EventAlreadyStarted, self).__init__(event_id)
        except TypeError:
            super().__init__(event_id)

    def __str__(self):
        return self.message


class EventAlreadyComplete(RuntimeError):
    """Raise when event is already complete."""
    def __init__(self, event_id=None):
        if event_id:
            self.message = """
                Event is already COMPLETED and has ID: {0},
                you need instantiate new object of this class
                to send new event.""".format(event_id)
        else:
            self.message = """
                Event is already COMPLETED.
                You need instantiate new object of this class
                to send new event."""
        try:
            super(EventAlreadyComplete, self).__init__(event_id)
        except TypeError:
            super().__init__(event_id)

    def __str__(self):
        return self.message
