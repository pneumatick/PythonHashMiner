import sys
import hashlib

def main():
    data = sys.argv[1]
    target = sys.argv[2]
    nonce = 0
    sha256_hash = hashlib.sha256(data.encode())
    hash_copy = sha256_hash.copy()
    
    hash_copy.update(str(nonce).encode())
    while hash_copy.hexdigest()[:len(target)] != target:
        hash_copy = sha256_hash.copy()
        nonce += 1
        hash_copy.update(str(nonce).encode())

    print("Data: " + data)
    print("Nonce: " + str(nonce))
    print("Raw string: " + data + str(nonce))
    print("Final hash: " + hash_copy.hexdigest())

main()
