from itertools import product

def permute_braces(A, B, C):
	if all(val == 0 for val in (A, B, C)):
		yield ""
		return 


	for a, b, c in product(range(A), range(B+1), range(C+1)):
		for first, second in product(permute_braces(a, b, c), permute_braces(A-a-1, B-b, C-c)):
			yield "(%s)%s" % (first, second)
	for a, b, c in product(range(A+1), range(B), range(C+1)):															
		for first, second in product(permute_braces(a, b, c), permute_braces(A-a, B-b-1, C-c)):
			yield "[%s]%s" % (first, second)
	for a, b, c in product(range(A+1), range(B+1), range(C)):
		for first, second in product(permute_braces(a, b, c), permute_braces(A-a, B-b, C-c-1)):
			yield "{%s}%s" % (first, second)


if __name__ == "__main__":
	for permutation in permute_braces(*[int(input()) for i in range(3)]):
		print(permutation)