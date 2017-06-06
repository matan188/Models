class Person:
    """ Base class to represent an individual, has vision and a type """
    def __init__(self, type, v=7):
        self._v = v
        self._type = type

    def get_type(self):
        return self._type

    def get_vision(self):
        return self._v
