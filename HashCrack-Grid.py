import hashlib
import os

def read_hash_from_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

def read_wordlist(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def check_hash(text, target_hash, hash_type):
    if hash_type == "MD5":
        return hashlib.md5(text.encode()).hexdigest() == target_hash
    elif hash_type == "SHA1":
        return hashlib.sha1(text.encode()).hexdigest() == target_hash
    elif hash_type == "SHA256":
        return hashlib.sha256(text.encode()).hexdigest() == target_hash
    elif hash_type == "SHA512":
        return hashlib.sha512(text.encode()).hexdigest() == target_hash
    else:
        return False

def identify_hash_type(hash_value):
    length = len(hash_value)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA1"
    elif length == 64:
        return "SHA256"
    elif length == 128:
        return "SHA512"
    else:
        raise ValueError("Unsupported hash type.")

def display_grid(rows, columns, values):
    os.system('clear')
    print("    ", end="")
    for col in range(columns):
        print(f"{col:>3}", end=" ")
    print()

    for row in range(rows):
        print(f"{row:>2} ", end="")
        for col in range(columns):
            print(f"[{values[row][col]}]", end=" ")
        print()

def brute_force_with_wordlist(rows, columns, target_hash, wordlist, hash_type):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()-_=+"

    grid = [[chars[(r + c) % len(chars)] for c in range(columns)] for r in range(rows)]
    display_grid(rows, columns, grid)

    for word_index, word in enumerate(wordlist):
        for r in range(rows):
            for c in range(columns):
                grid[r][c] = chars[(word_index + r + c) % len(chars)]

        if word_index % 10 == 0:
            display_grid(rows, columns, grid)

        if check_hash(word, target_hash, hash_type):
            print(f"\nHash Cracked! Password: {word}")
            return word

    return None

hash_file = 'hash.txt'
wordlist_file = 'wordlist.txt'

target_hash = read_hash_from_file(hash_file)
hash_type = identify_hash_type(target_hash)
wordlist = read_wordlist(wordlist_file)

rows = 5
columns = 12

cracked_password = brute_force_with_wordlist(rows, columns, target_hash, wordlist, hash_type)

if cracked_password:
    print(f"Hash Cracked: {cracked_password}")
else:
    print("No match found.")
