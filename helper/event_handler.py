class EventHandler:
    listeners = {}

    @classmethod
    def add_listener(cls, event, callback):
        if event not in cls.listeners:
            cls.listeners[event] = []
        cls.listeners[event].append(callback)

    @classmethod
    def emit(cls, event, *args, **kwargs):
        if event in cls.listeners:
            for callback in cls.listeners[event]:
                callback(*args, **kwargs)
