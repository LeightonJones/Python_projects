from math import log


num = int(input())
base = int(input())

if base <= 1:
    print(round(log(num), 2))
else:
    print(round(log(num, base), 2))

