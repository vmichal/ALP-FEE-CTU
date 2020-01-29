

def generator(n):
	while n >0:
		yield n
		n -= 1

for i in generator(10):
	print(i)
