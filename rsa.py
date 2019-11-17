import random
import gmpy2


#Euclid's GCD algorithm
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


#Euclid's extended algorithm for finding the multiplicative inverse of a number
def multiplicative_inverse(e, phi):
    r1 = phi
    r2 = e
    t1 = 0
    t2 = 1
    
    while r2 > 0:
        q = r1//r2
        r = r1 % r2
        r1 = r2
        r2 = r
        
        t = t1 - q*t2
        t1 = t2
        t2 = t
        
    if r1 == 1:
        return t1%phi


#Tests to see if a number is prime.
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
        
    n = p * q

    #phi(n)
    phi = (p-1) * (q-1)

    #Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    #Using Euclid's Algorithm to verify that e and phi(n) are comprime
    #If coprime, GCD is 1
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Use Extended Euclid's Algorithm to generate the private key, multiplicative inverse of e
    d = multiplicative_inverse(e, phi)
    
    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [gmpy2.powmod(ord(char), key, n) for char in plaintext]
    #Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr(gmpy2.powmod(char, key, n)) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)
    

if __name__ == '__main__':
    p = int(input("Enter a prime number p: "))
    q = int(input("Enter another prime number q (Different from above): "))
    
    public, private = generate_keypair(p, q)

    message = str(input("Enter a message to encrypt with the private key: "))

    print('\nPublic key: ', public)
    print('Private key: ', private)
    
    encrypted_msg = encrypt(private, message)
    print("\nEncrypted message: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("\nDecrypted message:")
    print(decrypt(public, encrypted_msg))
