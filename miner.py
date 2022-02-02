import sys
import hashlib

# Iterate the nonce and use it to update the copied data hash.
# Returns the nonced hash (class '_hashlib.HASH'), and the nonce (int).
def newHash(copiedDataHash, nonce):
    nonce += 1
    copiedDataHash.update(str(nonce).encode())
    return copiedDataHash, nonce

def main():
    data = sys.argv[1]
    target = sys.argv[2]
    nonce = 0
    sha256_hash = hashlib.sha256(data.encode())
    nonced_hash = sha256_hash.copy()              # Note: not nonced yet

    # Generate the first nonced hash
    nonced_hash.update(str(nonce).encode())

    # Loop until the user quits
    while True:
        # Add nonce to data('s context) and get the resulting hash. If the hash
        # does not resemble the target, iterate the nonce and repeat the process.
        while nonced_hash.hexdigest()[:len(target)] != target:
            nonced_hash, nonce = newHash(sha256_hash.copy(), nonce)

        # Print data
        print("Data: " + data)
        print("Nonce: " + str(nonce))
        print("Raw string: " + data + str(nonce))
        print("Final hash: " + nonced_hash.hexdigest())

        # Generate a new nonced hash
        nonced_hash, nonce = newHash(sha256_hash.copy(), nonce)

main()
