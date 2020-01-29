from sys import argv
from itertools import product
import queue

def print_matrix(matrix):
	for row in matrix:
		for stone in row:
			print(stone, end=' ')
		print()

def read_matrix(filename):
	result = []
	with open(filename) as infile:
		result = [list(map(int, row.split())) for row in infile]
	return result

def neighbours(matrix, y, x, target):
	res = []
	if y > 0:
		res.append((y-1,x))
	if x > 0:
		res.append((y, x-1))
	if y < len(matrix)-1:
		res.append((y+1, x))
	if x < len(matrix[0])-1:
		res.append((y, x+1))

	return res


def DFS(matrix, self_y, self_x, target, visited):
	result = [(self_y, self_x)]
	visited[self_y][self_x] = True
	free = False
	for y,x in neighbours(matrix, self_y, self_x, target):
		if matrix[y][x] == 0:
			free = True

		elif matrix[y][x] == target and not visited[y][x]:
			r, f = DFS(matrix, y, x, target, visited)
			result.extend(r)
			free = free or f

	return result, free
	

def eliminate_stones(matrix, target):
	height, width = len(matrix), len(matrix[0])
	visited = [[False]*width for i in range(height)]
	elimination_done = False

	for y, x in product(range(height), range(width)):
		if matrix[y][x] != target or visited[y][x]:
			continue
		component, free = DFS(matrix, y, x, target, visited)

		if not free:
			elimination_done = True
			for y, x in component:
				matrix[y][x] = 0
		else:
			for y,x in component:
				visited[y][x] = True

	return elimination_done




if __name__ == '__main__':
	matrix = read_matrix(argv[1])

	eliminate_stones(matrix, 1)

	if eliminate_stones(matrix, 2):
		print("ERROR")
	else:
		print_matrix(matrix)
		
