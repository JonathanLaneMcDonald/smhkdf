
from sys import argv
import base64
import getpass

from smhkdf import mhkdf

difficulty = {
	"weak": {
		"mod": 100,
		"match": 100
	},
	"medium": {
		"mod": 1000,
		"match": 1000
	},
	"strong": {
		"mod": 10000,
		"match": 10000
	},
	"recovery": {
		"mod": 100000,
		"match": 100000
	}
}

if __name__ == "__main__":

	assert len(argv) < 2 or argv[1] in difficulty.keys(), f"Valid args include {difficulty.keys()}"

	username = input("user >")
	password = getpass.getpass(prompt="pass >")

	key = mhkdf(username, password, difficulty[argv[1]]["mod"], difficulty[argv[1]]["match"])

	print(f"b64: {base64.b64encode(key).decode('utf-8')}")
	print(f"b85: {base64.b85encode(key).decode('utf-8')}")
