from random import randint


n = [[randint(0, 10), randint(0, 10)] for _ in range(randint(0, 20))]
print(n)

n = sum(n, [])
print(n)
