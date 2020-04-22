import random
import math

# Extended Euclidean algorithm
def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b%a, a)
		return (g, x-(b//a)*y, y)

# Modular inverse
def inverse(a, n):
	g, x, y = egcd(a, n)
	if g != 1:
		raise Exception("The two numbers are not coprime")
	else:
		return x%n

# Miller-Rabins test for n using k rounds
def mr(n, k):
	d = n-1
	r = 0
	while d%2==0:
		d /= 2
		r += 1

	d = int(d)
	r = int(r)

	def test_value(a):
		x = pow(a, d, n)
		if x==1 or x==n-1:
			return True

		for j in range(r):
			x = pow(x, 2, n)
			if x == n-1:
				return True

		return False

	for i in range(k):
		a = random.randint(2, n-1)
		if test_value(a):
			return True

	return False


# Generates a random prime between a and p
def generate_prime(a, b):
	p = random.randint(a, b+1)

	if p%2 == 0:
		p += 1

	while True:
		if mr(p, 7):
			return p

		p += 2

# Generate public and private key pair
def generate_keys(digits):
	p = generate_prime(10**(digits), 10**(digits+1))
	q = generate_prime(10**(digits), 10**(digits+1))

	n = p*q

	phi = (p-1)*(q-1)

	e = random.randint(1, phi)
	g = math.gcd(e, phi)
	while g != 1:
		e = random.randint(1, phi)
		g = math.gcd(e, phi)

	d = inverse(e, phi)

	return ((e, n), (d, n))

# Encrypt text using public key
def encrypt(pk, text):
	key, n = pk
	encrypted_text = [pow(ord(char), key, n) for char in text]
	return encrypted_text

# Decypher text using private key
def decypher(pk, encrypted_text):
	key, n = pk
	return "".join([chr(pow(char, key, n)) for char in encrypted_text])


public_key, private_key = generate_keys(17)

print("Public key: " , public_key)
print("Private key: ", private_key)
text = "Hello father. How is life."
encrypted_text = encrypt(public_key, text)
print(encrypted_text)
decypehered_text = decypher(private_key, encrypted_text)
print(decypehered_text)