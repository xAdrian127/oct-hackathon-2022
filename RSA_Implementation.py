from RSA_Math import big_prime, gcd, lcm, invmod


def get_keys():
    t = 0
    while gcd(65537, t) != 1:
        prime_1 = big_prime()
        prime_2 = big_prime()
        t = lcm(prime_1 - 1, prime_2 - 1)
    public_key = prime_1 * prime_2
    private_key_gen = invmod(65537, t)
    private_key_1 = private_key_gen % (prime_1 - 1)
    private_key_2 = private_key_gen % (prime_2 - 1)
    p2_inv = invmod(prime_2, prime_1)
    private_keyset = prime_1, prime_2, private_key_1, private_key_2, p2_inv
    return public_key, private_keyset


def new_signature(public_key, private_keyset, file_hash):
    prime_1, prime_2, private_key_1, private_key_2, p2_inv = private_keyset
    data = int.from_bytes(file_hash.encode('utf-8'), byteorder="big")
    mod_exp_1 = pow(data, private_key_1, prime_1)
    mod_exp_2 = pow(data, private_key_2, prime_2)
    t = mod_exp_1 - mod_exp_2
    if t < 0:
        t += prime_1
    h = (p2_inv * t) % prime_1
    return (mod_exp_2 + h * prime_2) % public_key


def verify_signature(signature, public_key, file_hash):
    return int.to_bytes(pow(signature, 65537, public_key), length=64, byteorder="big").decode('utf-8') == file_hash
