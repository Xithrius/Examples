lst = range(1, 15)
x = [[y, z] for y, z in zip(lst[1::2], lst[::2])]
print(x)
