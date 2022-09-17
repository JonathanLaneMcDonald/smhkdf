
## smhkdf: Simple, Memory-Hard Key Derivation Function

I had to make a super secret account on a website somewhere, so I put together a little tool to help me strengthen more memorable passwords by putting them through a memory-hard proof of work function.

It's a pretty simple script. Go have a look!


## Details

A public value and a private value are combined and used to initialize a stack of hashes. Hashes are added to the stack until it reaches the desired depth, at which point, the top-most hash is returned to the user.

### Memory Hardness

Computation of the (n+1)th hash value involves random access of the stack of hashes created during this session, so it seems like it'd be computationally expensive to have to repeat all that computation to simulate storing thousands or millions of hashes. Memory hardness grows as [--matches] grows.

### Computational Hardness

Computational hardness derives from the requirement of finding a partial hash collision to generate the (n+1)th hash. The probability of finding a colliding hash is 1/[--modulus].

### Presets

A handful of "presets" are defined: ["easy", "medium", "hard", "recovery", "ultra_recovery"]

* The "easy" preset completes almost instantaneously. 
* Progressively higher levels require 10x more compute per retained hash and retain 10x more hashes.
* The "hard" preset computes a key in about 4 seconds on a Ryzen 5 5600X.

## Usage

Say I want to use a kdf to generate passwords for Reddit? Not so important, right? I might use something like this

	python smhkdf.py --memo for_reddit --modulus 1000 --matches 1000

or alternatively

	python smhkdf.py --memo random_string_you_can_email_to_yourself_or_something --modulus 1000 --matches 1000

or, using a preset, 

	python smhkdf.py --memo domain_name.com --preset hard

or, optionally print to cli (default is copy to clipboard),

	python smhkdf.py --memo domain_name.com --preset hard --print_to_cli

_Note: The clipboard is weird in Linux, but works properly on Mac and Windows. So to (myself and) my Linux friends, maybe use the --print_to_cli option :/_

and you'll be prompted for a secret that'll be used to create a key you can use

Say you've made an account to protect your favorite recipes (and you're very serious about it!). Maybe you'd use larger values for [--modulus] and [--matches] like this

	python smhkdf.py --memo recipe_website --modulus 10000 --matches 1000000

### Note: computational cost is proportional to [--modulus] x [--matches]

## Due Diligence / Liability

I'm not your mom. Didn't your parents ever tell you not to use code from randos on the internet? I made this repo so I could track this project (because I'm using it, myself ;)) If you want to use it, too, you're welcome, but have a look over the code and reason things through for yourself first and, if you find any problems, let me know! lol glhf