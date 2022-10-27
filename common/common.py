

def sign(val):
    if val == 0:
        return 0
    return val / abs(val)


class direction_vector:
    def __init__(self, init_direction):
        self._direction = [init_direction[0], init_direction[1]]
        self._move_sign = [sign(init_direction[0]), sign(init_direction[1])]

    @property
    def x(self):
        return self._direction[0]

    @property
    def y(self):
        return self._direction[1]

    @property
    def x_sign(self):
        return self._move_sign[0]

    @property
    def y_sign(self):
        return self._move_sign[1]

    @x.setter
    def x(self, value):
        self._direction[0] = value
        self._move_sign[0] = sign(value)

    @y.setter
    def y(self, value):
        self._direction[1] = value
        self._move_sign[1] = sign(value)

    def __getitem__(self, idx):
        return self._direction[abs(idx) % 2]

    def __setitem__(self, idx, value):
        self._direction[abs(idx) % 2] = value
        self._move_sign[abs(idx) % 2] = sign(value)