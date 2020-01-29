import math


def f(x):
    return x * ((x ** 3) / 2 - x**2 - 2 * x + 1)


negative_count = 0
max, max_index = -math.inf, 0
min, min_index = math.inf, 0

for index, argument in enumerate(map(float, input().split())):
    value = f(argument)
    if value < 0.0:
        negative_count += 1
    if value * (argument**2) < min:
        min = value * argument **2
        min_index = index
    if value > max:
        max = value
        max_index = index

print("%d %d %d" % (max_index, negative_count, min_index))



    
