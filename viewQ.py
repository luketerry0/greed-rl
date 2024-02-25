import numpy as np

# Load the array from the file
array = np.load('sarsa_100000.npy')

# View the item at the specified index
item = array[27][7]
print(item)