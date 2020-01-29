import sys
from fractions import gcd


def read_input():
	with open(sys.argv[1]) as matrix_file, open(sys.argv[2]) as dictionary_file:
		matrix = [line.strip() for line in matrix_file]
		dictionary = [line.strip() for line in dictionary_file]
		return (matrix, dictionary)


def find_character(char, matrix):
	return [ (x, y) for y, line in enumerate(matrix) for x, c in enumerate(line) if c == char ]


def get_word_vectors(positions):
	if len(positions) < 2:
		return []

	A = positions[0]
	vectors = [ (X[0] - A[0], X[1] - A[1]) for X in positions[1:]]

	for i in range(len(vectors)):
		if vectors[i][0] < 0:
			vectors[i] = (-vectors[i][0], -vectors[i][1])
		divisor = gcd(vectors[i][0], vectors[i][1])
		if divisor < 0:
			divisor = -divisor
		if (divisor != 1):
			vectors[i] = (vectors[i][0] // divisor, vectors[i][1] // divisor)

	return vectors

def validate(vectors):
	first = vectors[0]
	negative = (-first[0], -first[1])
	for vector in vectors[1:]:
		if vector != first and vector != negative:
			return False
	return True

def get_searched_string(matrix, point, vector):
	dx, dy = vector

	if dy == 0 and dx == 1:
		coordinates = [(x,point[1]) for x in range(len(matrix[0]))]
		return matrix[point[1]], coordinates,6 

	result = []

	x,y = point
	while x > 0 and y > 0 and y < len(matrix) - 1:
		x -= dx
		y -= dy
	coordinates = []

	while x < len(matrix[0]) and y < len(matrix) and y >= 0:
		result.append(matrix[y][x])
		coordinates.append( (x,y) )
		x += dx
		y += dy

	direction = 0
	if dy == -1 and dx == 1:
		direction = 7
	elif dy == 1 and dx == 1:
		direction = 5
	elif dy == 1 and dx == 0:
		direction = 4	

	return ''.join(result), coordinates, direction

def find_word(string, word, placeholders):

	for start in range(len(string) - len(word) + 1):
		index = 0
		while word[index] == string[start] or string[start] == '0':
			if string[start] == '0':
				placeholders -= 1
			start += 1
			index += 1
			if index == len(word):
				if placeholders > 0:
					return False, 0
				else:
					return True, start - len(word)
		start += 1
	return False, 0

if __name__ == '__main__':
	
	if len(sys.argv) != 3:
		print("Two arguments expected!")
		sys.exit(1)

	matrix, dic = read_input()

	zero_positions = find_character('0', matrix)
	#print("positions:")
	#print(zero_positions)


	vectors = get_word_vectors(zero_positions)
	#print("vectors:")
	#print(vectors)


	if not validate(vectors):
		print("NONEXIST")
		sys.exit(0)

	string, coordinates, direction = get_searched_string(matrix, zero_positions[0], vectors[0])
	#print("data: %s %d" % (string, direction))
	#print("coordinates: ")
	#print(coordinates)

	min_length = string.rfind('0') - string.find('0')
	for word in dic:
		if len(word) <= min_length or len(word) > len(string):
			continue
		result = find_word(string, word, len(zero_positions))
		if result[0]:
			
			coord = coordinates[result[1]]
			print("%d %d %d %s" % (coord[1], coord[0], direction,word))
			sys.exit(0)
		
		result = find_word(string, word[::-1], len(zero_positions))
		if result[0]:
			
			coord = coordinates[result[1] + len(word) - 1]
			print("%d %d %d %s" % (coord[1], coord[0], direction - 4,word))
			sys.exit(0)
	print("NONEXIST")



