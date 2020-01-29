import sys
from itertools import product

def read_matrix():
	with open(sys.argv[1]) as file:
		return [list(map(lambda x: 1 if x[0] == '-' else 0, line.split())) for line in file]

def calculate_histogram_heights(matrix):
	height, width = len(matrix), len(matrix[0])

	for y in range(1,height):
		for x in range(width):
			if matrix[y][x] == 1:
				matrix[y][x] += matrix[y - 1][x]

def max_histogram(row, best_area, y):
	indices = [-1]
	a, b = (-1,-1), (-1,-1)
	for current in range(len(row)):
		while len(indices) > 1 and row[current] < row[indices[-1]]:
			column_height = row[indices[-1]]
			indices.pop()
			area = column_height * (current - indices[-1]-1)
			if area > best_area:
				best_area = area
				b = (y, current-1)
				a = (y-column_height+1, indices[-1]+1)
				#print(f"Find better rectangle (area = {area}) from {a} to {b}")
		indices.append(current)
	while len(indices) > 1:
			column_height = row[indices[-1]]
			indices.pop()
			area = column_height * (len(row) - indices[-1]-1)
			if area > best_area:
				best_area = area
				b = (y, len(row)-1)
				a = (y-column_height+1, indices[-1]+1)
				#print(f"Find better rectangle (area = {area}) from {a} to {b}")
	return best_area, a, b
	

def find_largest_submatrix(matrix):
	height, width = len(matrix), len(matrix[0])
		
	best = 0
	start, end = (-1,-1), (-1,-1)
	best_area = 0
	for y, row in enumerate(matrix):
		area, a, b = max_histogram(row, best_area, y)
		if area > best_area:
			best_area = area
			start = a
			end = b
	return start, end
		

if __name__ == '__main__':
	matrix = read_matrix()
	#print_matrix(matrix)
	calculate_histogram_heights(matrix)
	#print("After modification:")
	#print_matrix(matrix)

	start, end = find_largest_submatrix(matrix)
	print(start[0], start[1])
	print(end[0], end[1])

	