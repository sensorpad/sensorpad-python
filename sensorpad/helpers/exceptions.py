class EventAlreadyStarted(RuntimeError):
    '''Raise when a specific subset of values in context of app is wrong'''
    def __init__(self, event_id):
        self.message = 'Event already started and has ID: {0}'.format(event_id)
        try:
            super(EventAlreadyStarted, self).__init__(event_id)
        except TypeError:
            super().__init__(event_id)

    def __str__(self):
        return self.message