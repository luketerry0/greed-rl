import numpy as np

file = "td_lambda_100.npy"
V = np.load(file)

for x in range(55):
    for y in range(15):
        if x == 27 and y == 7:
            print("@".ljust(5), end=" ")
        else:
            print(str(round(V[x][y], 3)).ljust(5), end=" ")
    print()