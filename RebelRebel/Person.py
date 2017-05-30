class Person:
    def __init__(self, type, v=7):
        self._v = v
        self._type = type

    def spot_to_move_to(self):
        pass

    def get_type(self):
        return self._type

    def get_vision(self):
        return self._v
