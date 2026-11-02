# 1. Simulation of the CIA Triad
import hashlib

# Confidentiality
pwd = input("Enter Password: ")

if pwd != "admin":
    print("Access Denied")
else:
    print("Access Granted")

    # Integrity
    msg = input("Enter Message: ")
    h1 = hashlib.sha256(msg.encode()).hexdigest()

    new_msg = input("Re-enter Message: ")
    h2 = hashlib.sha256(new_msg.encode()).hexdigest()

    if h1 == h2:
        print("Integrity Verified")
    else:
        print("Integrity Failed")

# Availability
print("System Available")

# 2.Role-Based Access Control (RBAC) System
role = input("Enter your role (Admin/Faculty/Student): ")

if role == "Admin":
    print("Access Granted")
    print("Permissions: Add, Edit, Delete, View")

elif role == "Faculty":
    print("Access Granted")
    print("Permissions: Enter Marks, View Students")

elif role == "Student":
    print("Access Granted")
    print("Permissions: View Marks")

else:
    print("Access Denied")

# 3. File Encryption Tool Using AES (Fernet)
from cryptography.fernet import Fernet

# Generate Encryption Key
key = Fernet.generate_key()
cipher = Fernet(key)

# Get Message
message = input("Enter text to encrypt: ")
data = message.encode()

# Encryption
encrypted_data = cipher.encrypt(data)

print("\nEncrypted Data:")
print(encrypted_data.decode())

# Decryption
decrypted_data = cipher.decrypt(encrypted_data)

print("\nDecrypted Data:")
print(decrypted_data.decode())

# 4. Block Cipher Modes and Padding
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Get Message
message = input("Enter message: ")

# Generate AES Key and IV
key = os.urandom(32)
iv = os.urandom(16)

# Apply PKCS7 Padding
padder = padding.PKCS7(128).padder()

padded_data = padder.update(message.encode()) + padder.finalize()

# Encryption Using AES-CBC
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

encryptor = cipher.encryptor()

ciphertext = encryptor.update(padded_data) + encryptor.finalize()

print("\nEncrypted Data:")
print(ciphertext.hex())

# Decryption
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

decryptor = cipher.decryptor()

decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

# Remove Padding
unpadder = padding.PKCS7(128).unpadder()

decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

print("\nDecrypted Data:")
print(decrypted_data.decode())

# 5.Brute-Force Performance Lab (DES vs Triple DES
import time

def brute_force(target_key, key_space):

    attempts = 0
    start_time = time.perf_counter()

    for key in key_space:
        attempts += 1

        if key == target_key:
            end_time = time.perf_counter()

            return attempts, end_time - start_time

    return attempts, time.perf_counter() - start_time


# Key Space
key_space = [f"{i:04d}" for i in range(10000)]

des_target = "7500"
triple_des_target = "9500"


# DES Simulation
des_attempts, des_time = brute_force(des_target, key_space)

print("DES Simulation")
print("Attempts:", des_attempts)
print("Time:", des_time, "seconds")


# Triple DES Simulation
tdes_attempts, tdes_time = brute_force(triple_des_target, key_space)

print("\nTriple DES Simulation")
print("Attempts:", tdes_attempts)
print("Time:", tdes_time, "seconds")


print("\nNote: This is a small simulation and not an actual DES/3DES attack.")

# 6.Mathematical RSA Key Generation
import math

# Select Prime Numbers
p = 61
q = 53

# Calculate n
n = p * q

# Calculate Euler's Totient
phi = (p - 1) * (q - 1)

# Select Public Exponent
e = 17

# Calculate Private Exponent
d = pow(e, -1, phi)

# Get Message
message = int(input("Enter a number less than 3233: "))

if 0 <= message < n:

    # Encryption
    ciphertext = pow(message, e, n)

    # Decryption
    decrypted = pow(ciphertext, d, n)

    print("\nPublic Key:", (e, n))
    print("Private Key:", (d, n))
    print("Encrypted Message:", ciphertext)
    print("Decrypted Message:", decrypted)

else:
    print("Invalid Input! Enter a number between 0 and 3232.")

# 7. Secure Hybrid Cryptography System
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

# Generate RSA Private Key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Generate RSA Public Key
public_key = private_key.public_key()

# Generate AES Key
aes_key = Fernet.generate_key()

cipher = Fernet(aes_key)

# Get Message
message = input("Enter message: ")

# Encrypt Message Using AES
encrypted_message = cipher.encrypt(message.encode())

# Encrypt AES Key Using RSA Public Key
encrypted_aes_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Decrypt AES Key Using RSA Private Key
decrypted_aes_key = private_key.decrypt(
    encrypted_aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Decrypt Original Message
decrypted_message = Fernet(decrypted_aes_key).decrypt(encrypted_message)

print("\nEncrypted AES Key:", encrypted_aes_key.hex()[:50], "...")
print("Encrypted Message:", encrypted_message.decode())
print("Decrypted Message:", decrypted_message.decode())

# 8. Digital Signature Verification
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

# Generate RSA Private Key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Generate Public Key
public_key = private_key.public_key()

# Get Message
message = input("Enter message: ").encode()

# Create Digital Signature
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print("\nDigital Signature Created.")

# Verify Digital Signature
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print("Signature Verification: Successful")

except InvalidSignature:
    print("Signature Verification: Failed")

# 9. Advanced Input Sanitization and SQL Injection Prevention
import sqlite3
import re

# Create Database Connection
connection = sqlite3.connect(":memory:")

cursor = connection.cursor()

# Create Users Table
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL
)
""")

# Insert Sample Data
cursor.executemany(
    "INSERT INTO users (username) VALUES (?)",
    [("admin",), ("faculty",), ("student",)]
)

# Get Username
username = input("Enter username: ")

# Validate Input
if not re.fullmatch(r"[A-Za-z0-9_]{1,20}", username):

    print("Invalid username format.")

else:

    # Parameterized SQL Query
    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()

    if result:
        print("User found:", result[0])

    else:
        print("User not found.")

# Close Connection
connection.close()

# 10. XSS Mitigation via Context-Aware Output Encoding
import sqlite3
import re

# Create Database Connection
connection = sqlite3.connect(":memory:")

cursor = connection.cursor()

# Create Users Table
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL
)
""")

# Insert Sample Data
cursor.executemany(
    "INSERT INTO users (username) VALUES (?)",
    [("admin",), ("faculty",), ("student",)]
)

# Get Username
username = input("Enter username: ")

# Validate Input
if not re.fullmatch(r"[A-Za-z0-9_]{1,20}", username):

    print("Invalid username format.")

else:

    # Parameterized SQL Query
    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()

    if result:
        print("User found:", result[0])

    else:
        print("User not found.")

# Close Connection
connection.close()
# ________________________________________________________________________________




