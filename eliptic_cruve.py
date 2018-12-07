import sympy

class EllipticCurve:

    O ="O";

    def __init__(self,a,b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        if isinstance(other, EllipticCurve):
            return self.a == other.a and self.b == other.b
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    @property
    def discriminant(self):
        return 4*a**3+27*b**2
class Point:

def __init__(self,ec):
    self.ec = ec
    self = ec.O

def __init__(self,ec,x,y):
    self.ec = ec
    self.x = x
    self.y = y

def __add__(self, other):

    if self.ec != other.ec:
        raise ValueError('These points are on different curves')
    if self == self.ec.O:
        return Point(ec, other.x, other.y)
    if other == self.ec.O:
        return Point(ec, self.x, self.y)
    if self.x==other.x and self.y==-other.y:
        return O
    if self==other:
        k = 3*(self.x**2+self.ec.a)/(2*self.y)
        x3 = k**2-self.x-other.x
        return Point(self.ec, x3,k*(self.x-x3)-self.y)

    k = (other.y-self.y)/(other.x-self.x)
    x3 = k ** 2 - self.x - other.x
    return Point(self.ec, x3, k*(self.x - x3) - self.y)

def __eq__(self, other):
    if isinstance(other, Point):
        return self.x == other.x and self.y == other.y and self.ec == other.ec
    return NotImplemented

def __ne__(self, other):
    result = self.__eq__(other)
    if result is NotImplemented:
        return result
    return not result

def __neg__(self):
    if self==self.ec.O:
        return O
    return Point(E,self.x,-self.y)

def __sub__(self, other):
    return self + -other
