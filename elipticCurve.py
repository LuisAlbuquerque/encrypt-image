from sympy.abc import x, y
from sympy.core.compatibility import is_sequence
from sympy.core.numbers import oo
from sympy.core.relational import Eq
from sympy.polys.domains import FiniteField, QQ, RationalField
from sympy.solvers.solvers import solve

from sympy.ntheory.factor_ import divisors
from sympy.ntheory.residue_ntheory import sqrt_mod


class EllipticCurve():
    """
    Create the following Elliptic Curve over domain.
    `y^{2} + a_{1} x y + a_{3} y = x^{3} + a_{2} x^{2} + a_{4} x + a_{6}`
    The default domain is ``QQ``. If no coefficient ``a1``, ``a2``, ``a3``,
    it create curve as following form.
    `y^{2} = x^{3} + a_{4} x + a_{6}`
    Examples
    ========
    References
    ==========
    [1] J. Silverman "A Friendly Introduction to Number Theory" Third Edition
    [2] http://mathworld.wolfram.com/EllipticDiscriminant.html
    [3] G. Hardy, E. Wright "An Introduction to the Theory of Numbers" Sixth Edition
    """

    def __init__(self, a1, a2, a3, a4, a6, domain=QQ):
        self._dom = domain
        # Calculate discriminant
        self._b2 = a1**2 + 4 * a2
        self._b4 = 2 * a4 + a1 * a3
        self._b6 = a3**2 + 4 * a6
        self._b8 = a1**2 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3**2 - a4**2
        self._discrim = self._dom(-self._b2**2 * self._b8 - 8 * self._b4**3 - 27 * self._b6**2 + 9 * self._b2 * self._b4 * self._b6)
        self._a1 = self._dom(a1)
        self._a2 = self._dom(a2)
        self._a3 = self._dom(a3)
        self._a4 = self._dom(a4)
        self._a6 = self._dom(a6)
        self._eq = Eq(y**2 + self._a1*x*y + self._a3*y, x**3 + self._a2*x**2 + self._a4*x + self._a6)
        if isinstance(self._dom, FiniteField):
            self._rank = 0
        elif isinstance(self._dom, RationalField):
            self._rank = None

    @classmethod
    def minimal(cls, a4, a6, domain=QQ):
        return cls(0, 0, 0, a4, a6, domain)

    def __call__(self, x, y, z=1):
        if z == 0:
            return InfinityPoint(self)
        return Point(x, y, z, self)

    def __contains__(self, point):
        if is_sequence(point):
            if len(point) == 2:
                z1 = 1
            else:
                z1 = point[2]
            x1, y1 = point[:2]
        elif isinstance(point, Point):
            x1, y1, z1 = point.x, point.y, point.z
        else:
            raise ValueError('Invalid point.')
        if self.characteristic == 0 and z1 == 0:
            return True
        return self._eq.subs({x: x1, y: y1})

    def __repr__(self):
        return 'E({}): {}'.format(self._dom, self._eq)

    def points(self):
        """
        Return points of curve over Finite Field.
        Examples
        ========
        >>> from sympy.polys.domains import FF
        >>> from ec import EllipticCurve
        >>> e2 = EllipticCurve.minimal(1, 0, domain=FF(2))
        >>> list(e2.points())
        [(0, 0), (1, 0)]
        """
        char = self.characteristic
        if char > 1:
            for i in range(char):
                y = sqrt_mod(i**3 + self._a2*i**2 + self._a4*i + self._a6, char)
                if y is not None:
                    yield self(i, y)
                    if y != 0:
                        yield self(i, char - y)
        else:
            raise NotImplementedError("Still not implemented")

    def to_minimal(self):
        """
        Return minimal Weierstrass equation.
        Examples
        ========
        >>> from ec import EllipticCurve
        >>> e1 = EllipticCurve(0, -1, 1, -10, -20)
        >>> e1.to_minimal()
        E(QQ): y**2 == x**3 - 13392*x - 1080432
        """
        char = self.characteristic
        if char == 2:
            return self
        if char == 3:
            return EllipticCurve(0, self._b2/4, 0, self._b4/2, self._b6/4, self._dom)
        c4 = self._b2**2 - 24*self._b4
        c6 = -self._b2**3 + 36*self._b2*self._b4 - 216*self._b6
        return EllipticCurve.minimal(-27*c4, -54*c6, self._dom)

    def torsion_points(self):
        """
        Return torsion points of curve over Rational number.
        Return point objects those are finite order.
        According to Nagell-Lutz theorem, torsion point p(x, y)
        x and y are integers, either y = 0 or y**2 is divisor
        of discriminent. According to Mazur's theorem, there are
        at most 15 points in torsion collection.
        Examples
        ========
        >>> from ec import EllipticCurve
        >>> e2 = EllipticCurve.minimal(-43, 166)
        >>> [i for i in e2.torsion_points()]
        [O, (3, 8), (3, -8), (-5, 16), (-5, -16), (11, 32), (11, -32)]
        """
        if self.characteristic > 0:
            raise ValueError("No torsion point for Finite Field.")
        yield InfinityPoint(self)
        for x in solve(self._eq.subs(y, 0)):
            if x.is_rational:
                yield self(x, 0)
        for i in divisors(self.discriminant, generator=True):
            j = int(i**.5)
            if j**2 == i:
                for x in solve(self._eq.subs(y, j)):
                    p = self(x, j)
                    if x.is_rational and p.order() != oo:
                        yield p
                        yield -p

    @property
    def characteristic(self):
        """
        Return domain characteristic.
        Examples
        ========
        >>> from ec import EllipticCurve
        >>> e2 = EllipticCurve.minimal(-43, 166)
        >>> e2.characteristic
        0
        """
        return self._dom.characteristic()

    @property
    def discriminant(self):
        """
        Return curve discriminant.
        Examples
        ========
        >>> from ec import EllipticCurve
        >>> e2 = EllipticCurve.minimal(0, 17)
        >>> e2.discriminant
        -124848
        """
        return int(self._discrim)

    @property
    def is_singular(self):
        """
        Return True if curve discriminant is equal to zero.
        """
        return self.discriminant == 0

    @property
    def j_invariant(self):
        """
        Return curve j-invariant.
        Examples
        ========
        >>> from ec import EllipticCurve
        >>> e1 = EllipticCurve(0, 1, 1, -2, 0)
        >>> e1.j_invariant
        1404928/389
        """
        c4 = self._b2**2 - 24*self._b4
        return self._dom.to_sympy(c4**3 / self._discrim)

    @property
    def order(self):
        """
        Number of points in Finite field.
        Examples
        ========
        >>> from sympy.polys.domains import FF
        >>> from ec import EllipticCurve
        >>> e2 = EllipticCurve.minimal(1, 0, domain=FF(19))
        >>> e2.order
        19
        """
        if self.characteristic == 0:
            raise NotImplementedError("Still not implemented")
        return len(list(self.points()))

    @property
    def rank(self):
        """
        Number of independent points of infinite order.
        For Finite field, it must be 0.
        """
        if self._rank is not None:
            return self._rank
        raise NotImplementedError("Still not implemented")

EC = EllipticCurve


class Point():
    """
    Point of Elliptic Curve
    Examples
    ========
    >>> from ec import EllipticCurve
    >>> from sympy.polys.domains import FF
    >>> e1 = EllipticCurve.minimal(-17, 16)
    >>> p1 = e1(0, -4, 1)
    >>> p2 = e1(1, 0)
    >>> p1 + p2
    (15.0, -56.0)
    >>> e3 = EllipticCurve.minimal(-1, 9)
    >>> e3(1, -3) * 3
    (664/169, 17811/2197)
    >>> e2 = EC(0, 1, 1, -2, 0)
    >>> p = e2(-1,1)
    >>> q = e2(0, -1)
    >>> p + q
    (4.0, 8.0)
    >>> p - q
    (1, 0)
    >>> 3*p - 5*q
    (328/361, -2800/6859)
    >>> e4 = EllipticCurve.minimal(-5, 8, domain=FF(37))
    >>> p, q = e4(6, 3), e4(9, 10)
    >>> 3*p + 4*q
    (31, 28)
    """

    def __init__(self, x, y, z, curve):
        self.x = x
        self.y = y
        self.z = z
        self._curve = curve

    def __add__(self, p):
        x1, y1 = self.x, self.y
        x2, y2 = p.x, p.y
        a1 = self._curve._a1
        a2 = self._curve._a2
        a3 = self._curve._a3
        a4 = self._curve._a4
        a6 = self._curve._a6
        if x1 != x2:
            slope = (y1 - y2) / (x1 - x2)
            yint = (y1 * x2 - y2 * x1) / (x2 - x1)
        else:
            if (y1 + y2) == 0:
                return InfinityPoint(self._curve)
            slope = (3 * x1**2 + 2*a2*x1 + a4 - a1*y1) / (a1 * x1 + a3 + 2 * y1)
            yint = (-x1**3 + a4*x1 + 2*a6 - a3*y1) / (a1*x1 + a3 + 2*y1)
        x3 = slope**2 + a1*slope - a2 - x1 - x2
        y3 = -(slope + a1) * x3 - yint - a3
        return Point(x3, y3, 1, self._curve)

    def __mul__(self, n):
        n = int(n)
        r = InfinityPoint(self._curve)
        if n == 0:
            return r
        if n < 0:
            return -self * -n
        p = self
        while n:
            if n & 1:
                r = r + p
            n >>= 1
            p = p + p
        return r

    def __rmul__(self, n):
        return self * n

    def __neg__(self):
        return Point(self.x, -self.y - self._curve._a1*self.x - self._curve._a3, self.z, self._curve)

    def __repr__(self):
        try:
            return '({}, {})'.format(self.x.val, self.y.val)
        except AttributeError:
            pass
        return '({}, {})'.format(self.x.__str__(), self.y.__str__())

    def __sub__(self, other):
        return self + -other

    def order(self):
        """
        Return point order n where nP = 0.
        """
        if self.y == 0:  # P = -P
            return 2
        p = self * 2
        if p.y == -self.y:  # 2P = -P
            return 3
        i = 2
        while int(p.x) == p.x:
            p = self + p
            i += 1
            if isinstance(p, InfinityPoint):
                return i
        return oo


class InfinityPoint(Point):
    """
    Point at infinity of Elliptic Curve
    """

    def __init__(self, curve):
        super().__init__(0, 1, 0, curve)

    def __add__(self, p):
        return p

    def __neg__(self):
        return self

    def __radd__(self, p):
        return p

    def __repr__(self):
        return 'O'

    def order(self):
        return 1
