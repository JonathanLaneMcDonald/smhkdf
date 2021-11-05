
import argparse
import base64
import getpass
from hashlib import sha256
from tqdm import tqdm


def mhkdf(public, secret, modulus, matches):

	hash_stack = [sha256(sha256(public.encode("utf-8")).digest() + sha256(secret.encode("utf-8")).digest()).digest()]

	for _ in tqdm(range(len(hash_stack), matches)):
		ref = sha256(hash_stack[-1]).digest()
		ptr = int.from_bytes(ref, "big") % len(hash_stack)
		mod = int.from_bytes(sha256(ref + hash_stack[ptr]).digest(), "big") % modulus

		while int.from_bytes(ref, "big") % modulus != mod:
			ref = sha256(ref).digest()

		hash_stack.append(ref)

	return hash_stack[-1]


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--memo", type=str, required=True)
	parser.add_argument("--modulus", type=int, required=True)
	parser.add_argument("--matches", type=int, required=True)

	args = parser.parse_args()

	secret = getpass.getpass(prompt="--secret:")

	key = mhkdf(args.memo, secret, args.modulus, args.matches)

	print(f"b64: {base64.b64encode(key).decode('utf-8')}")
	print(f"b85: {base64.b85encode(key).decode('utf-8')}")
