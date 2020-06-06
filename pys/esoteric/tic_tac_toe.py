w = [0] * 16
a = [['*'] * 3 for _ in [0] * 3]
p = 1
c = int
v = {1: 'X', -2: 'O'}
P = print
W = {0: 147, 1: 15, 2: 168, 10: 24, 11: 2578, 12: 26, 20: 348, 21: 35, 22: 376}
while 3 not in w:
    for n in a:
        P(n)
    n = c(input())
    a[c(n / 10)][n % 10] = v[p]
    n = list(str(W[n]))
    p = ~p
    for N in n:
        w[(abs(p) - 1) * 8 + (c(N) - 1)] += 1
P(f"{v[~p]} won.")
