import math
import random
import warnings
import hashlib

# Euclidean algorithm for gcd computation
# Output: gcd g, Bezout's coefficients s, t such that g = s * a + t * b
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

# Modular inversion computation
def mod_inv(a, p):
    if a < 0:
        return p - mod_inv(-a, p)
    g, x, y = egcd(a, p)
    if g != 1:
        raise ArithmeticError("Modular inverse does not exist")
    else:
        return x % p

# Function to map a message to a bit string
def hash_message_to_bits(msg):
    h = hashlib.sha256()
    h.update(msg.encode())
    h_as_bits = ''.join(format(byte, '08b') for byte in h.digest())
    return h_as_bits

# Function to map a truncated bit string to an integer modulo q
def bits_to_int(h_as_bits, q):
    val = 0
    len = int(math.log(q, 2) + 1)
    for i in range(len):
        val = val * 2
        if(h_as_bits[i] == '1'):
            val = val + 1
    return val % q

#custom method to convert integers to sequence of bits; stored as list of bools
def int_to_bit_seq(n):
    bit_seq = []
    while n > 0:
        b = (n % 2) == 1
        n //= 2 #integer division to remove trailing floating point "floor"
        bit_seq.append(b)
    return bit_seq

# An elliptic curve is represented as an object of type Curve. 
# Note that for this lab, we use the short Weierstrass form of representation.
class Curve(object):

    def __init__(self, a, b, p, P_x, P_y, q):
        self.a = a
        self.b = b
        self.p = p
        self.P_x = P_x
        self.P_y = P_y
        self.q = q

    def is_singular(self):
        return (4 * self.a**3 + 27 * self.b**2) % self.p == 0

    def on_curve(self, x, y):
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0

    def is_equal(self, other):
        if not isinstance(other, Curve):
            return False
        return self.a == other.a and self.b == other.b and self.p == other.p

# A point at infinity on an elliptic curve is represented separately as an object of type PointInf. 
# We make this distinction between a point at infinity and a regular point purely for the ease of implementation.
class PointInf(object): #call point at infinity = p_inf; checked

    def __init__(self, curve):
        self.curve = curve

    def is_equal(self, other):
        if not isinstance(other, PointInf):
            return False
        return self.curve.is_equal(other.curve)

    def negate(self): 
        # Write a function that negates a PointInf object.        
        # Ths is an optional extension and is not evaluated
#        raise NotImplementedError()
        return self #p_inf is its own additive inverse; from slides

    def double(self): #checked
        # Write a function that doubles a PointInf object.
#        raise NotImplementedError()
        return self #p_inf + p_inf = p_inf from slides

    def add(self, other): #checked
        # Write a function that adds a Point object (or a PointInf object) to a PointInf object. 
        # See below for the description of a Point object
        # Make sure to output the correct kind of object depending on whether "other" is a Point object or a PointInf object
#        raise NotImplementedError()
        #either p_inf + non-p_inf or p_inf + p_inf
        #Check if other is either of type PointInf, Point, or something else (in this case throw exception)
        if isinstance(other, PointInf):
            return self #p_inf + p_inf = p_inf from slides
        if isinstance(other, Point):
            return other #non_p_inf + p_inf = non_p_inf; from slides
        raise TypeError("Variable _other_ has invalid type.")

# A point on an elliptic curve is represented as an object of type Point. 
# Note that for this lab, we will use 
# the affine coordinates-based representation of a point on an elliptic curve.
class Point(object):

    def __init__(self, curve, x, y):
        self.curve = curve
        self.x = x
        self.y = y
        self.p = self.curve.p
        self.on_curve = True
        if not self.curve.on_curve(self.x, self.y):
            warnings.warn("Point (%d, %d) is not on curve \"%s\"" % (self.x, self.y, self.curve))
            self.on_curve = False

    def is_equal(self, other):
        if not isinstance(other, Point):
            return False
        return self.curve.is_equal(other.curve) and self.x == other.x and self.y == other.y

    def negate(self): #checked
        # Write a function that negates a Point object and returns the resulting Point object
        # Ths is an optional extension and is not evaluated
#        raise NotImplementedError()
        return Point(self.curve, self.x, -self.y % self.p) #from slides

    def double(self): #checked
        # Write a function that doubles a Point object and returns the resulting Point object
#        raise NotImplementedError()
        #from module description; and slides
        #make it faster by storing the references
        x = self.x
        y = self.y
        p = self.p
        lambda_ = (3 * x**2 + self.curve.a) * mod_inv(2 * y, p) % p
        x_primed = (lambda_**2 - 2 * x) % p
        y_primed = (-(y + lambda_ * (x_primed - x))) % p
        return Point(self.curve, x_primed, y_primed)

    def add(self, other): #checked
        # Write a function that adds a Point object (or a PointInf object) to the current Point object and returns the resulting Point object
#        raise NotImplementedError()
        #check type of other: if PointInf, then return self. If non-Point type, throw exception. If type Point, compute accordingly to slides and module description.
        if isinstance(other, PointInf):
            return self
        if not isinstance(other, Point):
            raise TypeError("Variable _other_ has invalid type.")
        #From here on, other is of type Point
        #check special cases
        if self.is_equal(other):
            return self.double()
        #must check if points are on the same curve before proceeding with addition
        if not self.curve.is_equal(other.curve):
            raise ArithmeticError("Cannot add points on 2 different curves")
        #make it faster by storing the references
        x = self.x
        y = self.y
        ox = other.x
        oy = other.y
        p = self.p
        if x == ox and y != oy:
            #Then self = -other (other is the additive negative of self; follows from the intuition that for the reduced Weierstraass form a point on the elliptic curve must have 2 different values for y (because y**2) for the same x coordinate). Therefore the sum is the point at infinite.
            return PointInf(self.curve)
        #2 points on the curve; not identical nor identical x coordinates.
        lambda_ = ((y - oy) * mod_inv(x - ox, p)) % p
        x_primed = (lambda_**2 - x - ox) % p
        y_primed = (-(y + lambda_ * (x_primed - x))) % p
        return Point(self.curve, x_primed, y_primed)

    def scalar_multiply(self, scalar): #checked
        # Write a function that performs a scalar multiplication on the current Point object and returns the resulting Point object 
        # Make sure to check that the scalar is of type int or long
        # Your function need not be "constant-time"
#        raise NotImplementedError()
        #check scalar of type long or int
        if not isinstance(scalar, int): # (python3 does not have long) or (isinstance(scalar, long):
            raise TypeError("Scalar has not type int")
        #could check if point in question is the point at infinity but this is a class specifically not for this point
        if scalar == 0 or scalar == self.curve.q: #by definition
            return PointInf(self.curve)
        s = scalar % self.curve.q #module q because cyclic group of order q, assuming we are dealing here with a generator base point of order q, that lies on EC
        #from slides
        result = PointInf(self.curve)
        bit_sequence = int_to_bit_seq(s)
        for b in reversed(bit_sequence): #bit sequence is reversed when using int_to_bit_seq; have to begin with MSB
            result = result.double() #result * 2
            if b:
                result = self.add(result) #result + P
        return result
                

    def scalar_multiply_Montgomery_Ladder(self, scalar):
        # Write a function that performs a "constant-time" scalar multiplication on the current Point object and returns the resulting Point object 
        # Make sure to check that the scalar is of type int or long
        # Implement an elementary timer to check that your implementation is indeed constant-time
        # This is not graded but is an extension for your to try out on your own
        raise NotImplementedError() #Omitted


# The parameters for an ECDSA scheme are represented as an object of type ECDSA_Params
class ECDSA_Params(object):
    def __init__(self, a, b, p, P_x, P_y, q):
        self.p = p
        self.q = q
        self.curve = Curve(a, b, p, P_x, P_y, q)
        self.P = Point(self.curve, P_x, P_y)


def KeyGen(params):
    # Write a function that takes as input an ECDSA_Params object and outputs the key pair (x, Q)
#    raise NotImplementedError()
    #from module description
    x = random.randint(1, params.q - 1)
    Q = params.P.scalar_multiply(x)
    return (x, Q)

def Sign_FixedNonce(params, k, x, msg):
    # Write a function that takes as input an ECDSA_Params object, a fixed nonce k, a signing key x, and a message msg, and outputs a signature (r, s)
#    raise NotImplementedError()
    #sanity check for some inputs; not necessary
    if not (1 <= k and k <= params.q - 1):
        raise RuntimeError("Invalid k")
    q = params.q
    h = bits_to_int(hash_message_to_bits(msg), q)
    P_primed = params.P.scalar_multiply(k)
    r = P_primed.x % q
    s = ((h + x * r) * mod_inv(k, q)) % q
    if (r == 0) or (s == 0): #are k's given such that this is never true?
        raise RuntimeError("Invalid signatures")
    return (r, s)
    
def Sign(params, x, msg):
    # Write a function that takes as input an ECDSA_Params object, a signing key x, and a message msg, and outputs a signature (r, s)
    # The nonce is to be generated uniformly at random in the appropriate range
#    raise NotImplementedError()
    q = params.q
    while True: #from module slides
        k = random.randint(1, params.q - 1)
        h = bits_to_int(hash_message_to_bits(msg), q)
        P_primed = params.P.scalar_multiply(k)
        r = P_primed.x % params.q
        s = ((h + x * r) * mod_inv(k, q)) % q
        if (r != 0) and (s != 0):
            return (r, s)

def Verify(params, Q, msg, r, s):
    # Write a function that takes as input an ECDSA_Params object, a verification key Q, a message msg, and a signature (r, s)
    # The output should be either 0 (indicating failure) or 1 (indicating success)
#    raise NotImplementedError()
    #sanity check on inpupts
    q = params.q
    if not ((1 <= r and r <= q - 1) and (1 <= s and s <= q - 1)):
        return 0
    h = bits_to_int(hash_message_to_bits(msg), q)
    w = mod_inv(s, q)
    u1 = w * h % q
    u2 = w * r % q
    Z = params.P.scalar_multiply(u1).add(Q.scalar_multiply(u2))
    if (r == Z.x % q):
        return 1
    return 0

from module_1_ECC_ECDSA_tests import run_tests
run_tests(ECDSA_Params, Point, KeyGen, Sign, Sign_FixedNonce, Verify)
