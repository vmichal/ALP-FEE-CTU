import sys
import queue

names = {}

with open(sys.argv[1]) as file:
	for line in file:
		name1, name2 = line.strip().split()
		for name in (name1, name2):
			if name not in names:
				names[name] = []

		names[name1].append(name2)
		names[name2].append(name1)


scores = {name : None for name in names }

q = queue.Queue()
scores['erdos'] = 0
q.put('erdos')

while not q.empty():
	current = q.get()
	if current == sys.argv[2]:
		print(scores[current])
		sys.exit()

	for neighbour in names[current]:
		if scores[neighbour] is None:
			scores[neighbour] = scores[current] + 1
			q.put(neighbour)

print("None") 