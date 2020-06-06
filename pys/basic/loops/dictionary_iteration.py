d = {1: 'two', 3.0: 'four', 5: 6.0}


for key in d:
    print(key)
print()

for key in d.keys():
    print(key)
print()

for value in d.values():
    print(value)
print()

for index, (key, value) in enumerate(d.items()):
    print(index, key, value)
print()
