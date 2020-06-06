from random import randint
import numpy as np


col_length = randint(2, 4)
n = [[randint(0, 10) for __ in range(col_length)] for _ in range(randint(4, 10))]
n = np.array(n)

for col in range(n.shape[1]):
    tmp = sorted([list(x) for x in list(n)], key=lambda d: d[col], reverse=True)
    print(f'Sorted by column index {col}: {tmp}')
