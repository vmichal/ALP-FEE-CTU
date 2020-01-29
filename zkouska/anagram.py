import sys
import itertools
import string


def letter_sum(str) -> int:
	result = 0
	for char in str:
		if char.upper() or char.lower():
			result += ord(char)

	return result

def are_anagrams(a, b):
	letters = {chr(letter) : 0 for letter in itertools.chain(range(ord('a'), ord('z') +1), range(ord('A'), ord('Z') +1))}

	for letter in a:
		if letter.isupper() or letter.islower():
			letters[letter] += 1

	for letter in b:
		if letter.isupper() or letter.islower():
			if letters[letter] == 0:
				return False
			letters[letter] -= 1

	for letter, count in letters.items():
		if count:
			return False
	return True

def find_anagrams(possibilities) -> list:
	possibilities.sort(key= lambda tuple : tuple[1])
	return [(a[1], b[1]) for a, b in itertools.product(possibilities, repeat=2) if a[1] < b[1] and are_anagrams(a[2],b[2])]



def main():
	lines = []
	with open(sys.argv[1]) as file:
		lines = [line.strip() for line in file]

	hashes = [(letter_sum(str), i, str) for i, str in enumerate(lines) ]
	hashes.sort(key=lambda tuple : tuple[0])


	anagrams = []
	index = 0
	for i in range(len(hashes)):

		similar = [tuple for tuple in hashes if hashes[0] == hashes[i]]
		anagrams += find_anagrams(similar)


	if len(anagrams) == 0:
		print("None")
		sys.exit()

	anagrams.sort()
	for anagram in anagrams:
		print("%d %d" % (anagram))


if __name__ == '__main__':
	main()