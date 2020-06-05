# Integers:
integer = 6
binaryInt = 0b1001  # == 9
octalInt = 0o43  # == 35
hexInt = 0xff0000  # == red

# Floats:
decimal = 4.2
exponential = 3.2e4  # == 3.2*10**4 == 32000

# Complex numbers:
complexNumber = complex(4, 6)  # 4 + 6i

# Strings:
string1 = "Hello World"
string2 = 'Hello World'

# Booleans:
boolean = True


# Data Structures:

# Lists (Mutable: can be changed. Ordered: Maintains order.)
lst = [4, 2, 5.3]

# Tuple (Immutable: cannot be changed. Ordered: Maintains order.)
t = (4, 2, 5.3)

# Set (Mutable: can be changed. Unordered: Cannot maintain order.)
s = {4, 6, 2}

# Dictionaries (Mutable: Can be changed. Ordered: Maintains order.)
d = {'a': 4, True: 3, 0: 's'}

d['a']  # == 4
d[True]  # == 3
d[0]  # == 's'

try:
    d['b']
except KeyError:
    pass
