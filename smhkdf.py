
import argparse
import getpass
import pyperclip

from base64 import b64encode, b85encode
from hashlib import sha256
from tqdm import tqdm


def mhkdf(public, secret, modulus, matches):

    hash_stack = [sha256(sha256(public.encode("utf-8")).digest() + sha256(secret.encode("utf-8")).digest()).digest()]

    for _ in tqdm(range(len(hash_stack), matches+1)):
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
    parser.add_argument("--modulus", type=int, default=None)
    parser.add_argument("--matches", type=int, default=None)
    parser.add_argument("--preset", type=str, default=None)
    parser.add_argument("--base64", action="store_true", default=False)
    parser.add_argument("--print_to_cli", action="store_true", default=False)

    args = parser.parse_args()

    presets = {
        "easy":             {"mod": 1,     "match": 1000},
        "medium":           {"mod": 10,    "match": 10000},
        "hard":             {"mod": 100,   "match": 100000},
        "recovery":         {"mod": 1000,  "match": 1000000},
        "ultra_recovery":   {"mod": 10000, "match": 10000000}
    }

    mod, match = None, None

    if args.preset is not None:
        if args.preset not in presets:
            raise ValueError(f"Preset {args.preset} not in {presets.keys()}")
        mod, match = presets[args.preset]["mod"], presets[args.preset]["match"]
    else:
        if args.modulus is None or args.matches is None:
            raise ValueError("Must define either a preset or modulus and matches")
        mod, match = args.modulus, args.matches

    key = mhkdf(args.memo, getpass.getpass(prompt="--secret:"), mod, match)

    deliverable_string = (b64encode(key) if args.base64 else b85encode(key)).decode('utf-8')

    if args.print_to_cli:
        print(deliverable_string)
    else:
        pyperclip.copy(deliverable_string)
        print(f"Copied {'base64' if args.base64 else 'base85'} password to clipboard")
