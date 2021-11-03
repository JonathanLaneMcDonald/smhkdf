
import argparse
import base64
import getpass
from hashlib import sha256


def mhkdf(public, secret, modulus, matches):

    public_bytes = sha256(public.encode("utf-8")).digest()
    secret_bytes = sha256(secret.encode("utf-8")).digest()

    hash_stack = [sha256(public_bytes + secret_bytes).digest()]

    hashes = 0
    while len(hash_stack) < matches:

        reference = hash_stack[-1]
        friend_pointer = int.from_bytes(reference, "big") % len(hash_stack)
        friend = hash_stack[friend_pointer]

        mixer = sha256(reference + friend).digest()
        mixer_match = int.from_bytes(mixer, "big") % modulus
        mixer = sha256(mixer).digest()

        while int.from_bytes(mixer, "big") % modulus != mixer_match:
            hashes += 1
            mixer = sha256(mixer).digest()

        hash_stack.append(mixer)

    print(f"sha256 Hashes: {hashes} hash stack length: {len(hash_stack)}")

    return hash_stack[-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", type=str)
    parser.add_argument("--modulus", type=int)
    parser.add_argument("--matches", type=int)

    args = parser.parse_args()

    secret = getpass.getpass(prompt="--secret:")

    key = mhkdf(args.public, secret, args.modulus, args.matches)

    print(f"b16: {base64.b16encode(key).decode('utf-8')}")
    print(f"b32: {base64.b32encode(key).decode('utf-8')}")
    print(f"b64: {base64.b64encode(key).decode('utf-8')}")
    print(f"b85: {base64.b85encode(key).decode('utf-8')}")
