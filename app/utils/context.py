class Context(object):
    def __init__(self, **kwargs):
        self._attributes = {}

        for key, value in kwargs.items():
            self._attributes[key] = value

    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]
        else:
            return None

    def __setattr__(self, name, value):
        if name == "_attributes":
            super().__setattr__(name, value)
        else:
            self._attributes[name] = value
