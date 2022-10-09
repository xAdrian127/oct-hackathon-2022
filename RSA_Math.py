import random

def gcd(a, b):
    '''Computes the Great Common Divisor using the Euclid's algorithm'''
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Computes the Lowest Common Multiple using the GCD method."""
    return a // gcd(a, b) * b


def exgcd(a, b):
    """Extended Euclidean Algorithm that can give back all gcd, s, t
    such that they can make Bézout's identity: gcd(a,b) = a*s + b*t
    Return: (gcd, s, t) as tuple"""
    old_s, s = 1, 0
    old_t, t = 0, 1
    while b:
        q = a // b
        s, old_s = old_s - q * s, s
        t, old_t = old_t - q * t, t
        a, b = b, a % b
    return a, old_s, old_t


def invmod(e, m):
    """Find out the modular multiplicative inverse x of the input integer
    e with respect to the modulus m. Return the minimum positive x"""
    g, x, y = exgcd(e, m)
    assert g == 1

    # Now we have e*x + m*y = g = 1, so e*x ≡ 1 (mod m).
    # The modular multiplicative inverse of e is x.
    if x < 0:
        x += m
    return x

# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def getLowLevelPrime(n):
    '''Generate a prime candidate divisible
    by first primes'''
    while True:
        # Obtain a random number
        pc = random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)

        # Test divisibility by pre-generated
        # primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor ** 2 <= pc:
                break
        else:
            return pc


def isMillerRabinPassed(mrc):
    '''Run 20 iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc - 1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert (2 ** maxDivisionsByTwo * ec == mrc - 1)

    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                return False
        return True

    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True


def big_prime():
    while True:
        n = 1500
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            return prime_candidate

