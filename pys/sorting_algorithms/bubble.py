from random import randint


n = [randint(0, 10) for _ in range(randint(0, 20))]
print(n)

check = True
while check:
    check = False
    for i in range(len(n) - 1):
        if n[i] > n[i + 1]:
            n[i], n[i + 1] = n[i + 1], n[i]
            check = True

print(n)
