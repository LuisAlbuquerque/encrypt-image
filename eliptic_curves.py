# Basics of Elliptic Curve Cryptography implementation on Python
import collections


def inv(n, q):
    """div on PN modulo a/b mod q as a * inv(b, q) mod q
    >>> assert n * inv(n, q) % q == 1
    """
    for i in range(q):
        if (n * i) % q == 1:
            return i
        pass
    assert False, "unreached"
    pass


def sqrt(n, q):
    """sqrt on PN modulo: returns two numbers or exception if not exist
    >>> assert (sqrt(n, q)[0] ** 2) % q == n
    >>> assert (sqrt(n, q)[1] ** 2) % q == n
    """
    assert n < q
    for i in range(1, q):
        if i * i % q == n:
            return (i, q - i)
        pass
    raise Exception("not found")


Coord = collections.namedtuple("Coord", ["x", "y"])


class EC(object):
    """System of Elliptic Curve"""
    def __init__(self, a, b, q):
        """elliptic curve as: (y**2 = x**3 + a * x + b) mod q
        - a, b: params of curve formula
        - q: prime number
        """
        assert 0 < a and a < q and 0 < b and b < q and q > 2
        assert (4 * (a ** 3) + 27 * (b ** 2))  % q != 0
        self.a = a
        self.b = b
        self.q = q
        # just as unique ZERO value representation for "add": (not on curve)
        self.zero = Coord(0, 0)
        pass

    def is_valid(self, p):
        if p == self.zero: return True
        l = (p.y ** 2) % self.q
        r = ((p.x ** 3) + self.a * p.x + self.b) % self.q
        return l == r

    def at(self, x):
        """find points on curve at x
        - x: int < q
        - returns: ((x, y), (x,-y)) or not found exception
        >>> a, ma = ec.at(x)
        >>> assert a.x == ma.x and a.x == x
        >>> assert a.x == ma.x and a.x == x
        >>> assert ec.neg(a) == ma
        >>> assert ec.is_valid(a) and ec.is_valid(ma)
        """
        assert x < self.q
        ysq = (x ** 3 + self.a * x + self.b) % self.q
        y, my = sqrt(ysq, self.q)
        return Coord(x, y), Coord(x, my)

    def neg(self, p):
        """negate p
        >>> assert ec.is_valid(ec.neg(p))
        """
        return Coord(p.x, -p.y % self.q)

    def add(self, p1, p2):
        """<add> of elliptic curve: negate of 3rd cross point of (p1,p2) line
        >>> d = ec.add(a, b)
        >>> assert ec.is_valid(d)
        >>> assert ec.add(d, ec.neg(b)) == a
        >>> assert ec.add(a, ec.neg(a)) == ec.zero
        >>> assert ec.add(a, b) == ec.add(b, a)
        >>> assert ec.add(a, ec.add(b, c)) == ec.add(ec.add(a, b), c)
        """
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
            # p1 + -p1 == 0
            return self.zero
        if p1.x == p2.x:
            # p1 + p1: use tangent line of p1 as (p1,p1) line
            l = (3 * p1.x * p1.x + self.a) * inv(2 * p1.y, self.q) % self.q
            pass
        else:
            l = (p2.y - p1.y) * inv(p2.x - p1.x, self.q) % self.q
            pass
        x = (l * l - p1.x - p2.x) % self.q
        y = (l * (p1.x - x) - p1.y) % self.q
        return Coord(x, y)

    def mul(self, p, n):
        """n times <mul> of elliptic curve
        >>> m = ec.mul(p, n)
        >>> assert ec.is_valid(m)
        >>> assert ec.mul(p, 0) == ec.zero
        """
        r = self.zero
        m2 = p
        # O(log2(n)) add
        while 0 < n:
            if n & 1 == 1:
                r = self.add(r, m2)
                pass
            n, m2 = n >> 1, self.add(m2, m2)
            pass
        # [ref] O(n) add
        #for i in range(n):
        #    r = self.add(r, p)
        #    pass
        return r

    def order(self, g):
        """order of point g
        >>> o = ec.order(g)
        >>> assert ec.is_valid(a) and ec.mul(a, o) == ec.zero
        >>> assert o <= ec.q
        """
        assert self.is_valid(g) and g != self.zero
        for i in range(1, self.q + 1):
            if self.mul(g, i) == self.zero:
                return i
            pass
        raise Exception("Invalid order")
    pass


class ElGamal(object):
    """ElGamal Encryption
    pub key encryption as replacing (mulmod, powmod) to (ec.add, ec.mul)
    - ec: elliptic curve
    - g: (random) a point on ec
    """
    def __init__(self, ec, g):
        assert ec.is_valid(g)
        self.ec = ec
        self.g = g
        self.n = ec.order(g)
        pass

    def gen(self, priv):
        """generate pub key
        - priv: priv key as (random) int < ec.q
        - returns: pub key as points on ec
        """
        return self.ec.mul(g, priv)

    def enc(self, plain, pub, r):
        """encrypt
        - plain: data as a point on ec
        - pub: pub key as points on ec
        - r: randam int < ec.q
        - returns: (cipher1, ciper2) as points on ec
        """
        assert self.ec.is_valid(plain)
        assert self.ec.is_valid(pub)
        return (self.ec.mul(g, r), self.ec.add(plain, self.ec.mul(pub, r)))

    def dec(self, cipher, priv):
        """decrypt
        - chiper: (chiper1, chiper2) as points on ec
        - priv: private key as int < ec.q
        - returns: plain as a point on ec
        """
        c1, c2 = cipher
        assert self.ec.is_valid(c1) and ec.is_valid(c2)
        return self.ec.add(c2, self.ec.neg(self.ec.mul(c1, priv)))
    pass


class DiffieHellman(object):
    """Elliptic Curve Diffie Hellman (Key Agreement)
    - ec: elliptic curve
    - g: a point on ec
    """
    def __init__(self, ec, g):
        self.ec = ec
        self.g = g
        self.n = ec.order(g)
        pass

    def gen(self, priv):
        """generate pub key"""
        assert 0 < priv and priv < self.n
        return self.ec.mul(self.g, priv)

    def secret(self, priv, pub):
        """calc shared secret key for the pair
        - priv: my private key as int
        - pub: partner pub key as a point on ec
        - returns: shared secret as a point on ec
        """
        assert self.ec.is_valid(pub)
        assert self.ec.mul(pub, self.n) == self.ec.zero
        return self.ec.mul(pub, priv)
    pass


class DSA(object):
    """ECDSA
    - ec: elliptic curve
    - g: a point on ec
    """
    def __init__(self, ec, g):
        self.ec = ec
        self.g = g
        self.n = ec.order(g)
        pass

    def gen(self, priv):
        """generate pub key"""
        assert 0 < priv and priv < self.n
        return self.ec.mul(self.g, priv)

    def sign(self, hashval, priv, r):
        """generate signature
        - hashval: hash value of message as int
        - priv: priv key as int
        - r: random int 
        - returns: signature as (int, int)
        """
        assert 0 < r and r < self.n
        m = self.ec.mul(self.g, r)
        return (m.x, inv(r, self.n) * (hashval + m.x * priv) % self.n)

    def validate(self, hashval, sig, pub):
        """validate signature
        - hashval: hash value of message as int
        - sig: signature as (int, int)
        - pub: pub key as a point on ec
        """
        assert self.ec.is_valid(pub)
        assert self.ec.mul(pub, self.n) == self.ec.zero
        w = inv(sig[1], self.n)
        u1, u2 = hashval * w % self.n, sig[0] * w % self.n
        p = self.ec.add(self.ec.mul(self.g, u1), self.ec.mul(pub, u2))
        return p.x % self.n == sig[0]
    pass


if __name__ == "__main__":
    # shared elliptic curve system of examples
    ec = EC(1, 18, 19)
    g, _ = ec.at(7)
    assert ec.order(g) <= ec.q
    
    # ElGamal enc/dec usage
    eg = ElGamal(ec, g)
    # mapping value to ec point
    # "masking": value k to point ec.mul(g, k)
    # ("imbedding" on proper n:use a point of x as 0 <= n*v <= x < n*(v+1) < q)
    mapping = [ec.mul(g, i) for i in range(eg.n)]
    plain = mapping[7] 
    
    priv = 5
    pub = eg.gen(priv)
    
    cipher = eg.enc(plain, pub, 15)
    decoded = eg.dec(cipher, priv)
    assert decoded == plain
    assert cipher != pub
    
    
    # ECDH usage
    dh = DiffieHellman(ec, g)
    
    apriv = 11
    apub = dh.gen(apriv)
    
    bpriv = 3
    bpub = dh.gen(bpriv)
    
    cpriv = 7
    cpub = dh.gen(cpriv)
    # same secret on each pair
    assert dh.secret(apriv, bpub) == dh.secret(bpriv, apub)
    assert dh.secret(apriv, cpub) == dh.secret(cpriv, apub)
    assert dh.secret(bpriv, cpub) == dh.secret(cpriv, bpub)
    
    # not same secret on other pair
    assert dh.secret(apriv, cpub) != dh.secret(apriv, bpub)
    assert dh.secret(bpriv, apub) != dh.secret(bpriv, cpub)
    assert dh.secret(cpriv, bpub) != dh.secret(cpriv, apub)
    
    
    # ECDSA usage
    dsa = DSA(ec, g)
    
    priv = 11
    pub = eg.gen(priv)
    hashval = 128
    r = 7
    
    sig = dsa.sign(hashval, priv, r)
    assert dsa.validate(hashval, sig, pub)
    pass


# Appendix: improved modulo calc

def inv(n, q):
    """div on PN modulo a/b mod q as a * inv(b, q) mod q
    >>> assert n * inv(n, q) % q == 1
    """
    # n*inv % q = 1 => n*inv = q*m + 1 => n*inv + q*-m = 1
    # => egcd(n, q) = (inv, -m, 1) => inv = egcd(n, q)[0] (mod q)
    return egcd(n, q)[0] % q
    #[ref] naive implementation
    #for i in range(q):
    #    if (n * i) % q == 1:
    #        return i
    #    pass
    #assert False, "unreached"
    #pass


def egcd(a, b):
    """extended GCD
    returns: (s, t, gcd) as a*s + b*t == gcd
    >>> s, t, gcd = egcd(a, b)
    >>> assert a % gcd == 0 and b % gcd == 0
    >>> assert a * s + b * t == gcd
    """
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b > 0:
        q, r = divmod(a, b)
        a, b = b, r
        s0, s1, t0, t1 = s1, s0 - q * s1, t1, t0 - q * t1
        pass
    return s0, t0, a

def inv2(n, q):
    """another PN invmod: from euler totient function
    - n ** (q - 1) % q = 1 => n ** (q - 2) % q = n ** -1 % q
    """
    assert q > 2
    s, p2, p = 1, n, q - 2
    while p > 0:
        if p & 1 == 1: s = s * p2 % q
        p, p2 = p >> 1, pow(p2, 2, q)
        pass
    return s


def sqrt(n, q):
    """sqrt on PN modulo: returns two numbers or exception if not exist
    >>> assert (sqrt(n, q)[0] ** 2) % q == n
    >>> assert (sqrt(n, q)[1] ** 2) % q == n
    """
    assert n < q
    for i in range(1, q):
        if pow(i, 2, q) == n:
            return (i, q - i)
        pass
    raise Exception("not found")


def sqrt2(n, q):
    """sqrtmod for bigint
    - Algorithm 3.34 of http://www.cacr.math.uwaterloo.ca/hac/about/chap3.pdf
    """
    import random
    # b: some non-quadratic-residue
    b = 0 
    while b == 0 or jacobi(b, q) != -1:
        b = random.randint(1, q - 1)
        pass
    # q = t * 2^s + 1, t is odd
    t, s = q - 1, 0 
    while t & 1 == 0:
        t, s = t >> 1, s + 1
        pass
    assert q == t * pow(2, s) + 1 and t % 2 == 1
    ni = inv(n, q)
    c = pow(b, t, q)
    r = pow(n, (t + 1) // 2, q)
    for i in range(1, s):
        d = pow(pow(r, 2, q) * ni % q, pow(2, s - i - 1, q), q)
        if d == q - 1: r = r * c % q
        c = pow(c, 2, q)
        pass
    return (r, q - r)


def jacobi(a, q):
    """jacobi symbol: judge existing sqrtmod (1: exist, -1: not exist)
    - j(a*b,q) = j(a,q)*j(b,q)
    - j(a*q+b, q) = j(b, q)
    - j(a, 1) = 1
    - j(0, q) = 0
    - j(2, q) = -1 ** (q^2 - 1)/8
    - j(p, q) = -1 ^ {(p - 1)/2 * (q - 1)/2} * j(q, p)
    """
    if q == 1: return 1
    if a == 0: return 0
    if a % 2 == 0: return (-1) ** ((q * q - 1) // 8) * jacobi(a // 2, q)
    return (-1) ** ((a - 1) // 2 * (q - 1) // 2) * jacobi(q % a, a)

def jacobi2(a, q):
    """quick jacobi symbol
    - algorithm 2.149 of http://www.cacr.math.uwaterloo.ca/hac/about/chap2.pdf
    """
    if a == 0: return 0
    if a == 1: return 1
    a1, e = a, 0
    while a1 & 1 == 0:
        a1, e = a1 >> 1, e + 1
        pass
    m8 = q % 8
    s = -1 if m8 == 3 or m8 == 5 else 1 # m8 = 0,2,4,6 and 1,7
    if q % 4 == 3 and a1 % 4 == 3: s = -s
    return s if a1 == 1 else s * jacobi2(q % a1, a1)

