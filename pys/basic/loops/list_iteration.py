lst = [1, 'two', 3.0]


for item in lst:
    print(item)
print()

for index in range(len(lst)):
    print(lst[index])
print()

for index, item in enumerate(lst):
    print(index, item)
print()

i = 0
while i != len(lst):
    print(lst[i])
    i += 1
print()
