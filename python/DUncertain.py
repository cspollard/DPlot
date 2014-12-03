from math import sqrt

# very simple library for uncertain values.

def quadsum(x, y):
    return sqrt(x**2 + y**2)

def usqrt(u):
    if u.x > 0:
        return Uncertain(sqrt(u.x), u.dx/(2*sqrt(u.x)))
    if u.x == 0:
        return Uncertain(0.0, 0.0)
    else:
        return Uncertain(None, 0)

class Uncertain:
    def __init__(self, x, dx):
        self.x = x
        self.dx = dx
        return

    def __add__(self, u):
        return Uncertain(self.x+u.x, quadsum(self.dx, u.dx))

    def __sub__(self, u):
        return self + (-u)

    def __mul__(self, u):
        return Uncertain(self.x*u.x,
                quadsum(self.x*u.dx, u.x*self.dx))

    def __neg__(self):
        return Uncertain(-self.x, self.dx)

    def recip(self):
        if self.x == 0:
            return Uncertain(0.0, 0.0)
        else:
            return Uncertain(1.0/self.x, self.dx/(self.x*self.x))

    def __div__(self, u):
        return self * u.recip()

    def __repr__(self):
        return "%s +/- %s" % (self.x, self.dx)
