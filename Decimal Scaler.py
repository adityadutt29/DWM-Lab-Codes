import numpy as np
import math

# Input Data
data = np.array([
    [10.0, -255.0, -5.0],
    [150.0, 180.0, 0.0],
    [5.0, 250.0, 110.0],
    [-1200.0, -210.0, -2.0]
], dtype=float)

s_data = data.copy()

for col in range(data.shape[1]):
    max_abs_val = np.max(np.abs(data[:, col]))
    if max_abs_val == 0:
        j = 1
    else:
        j = math.ceil(math.log10(max_abs_val))
    divisor = 10**j
    s_data[:, col] = data[:, col] / divisor

# Output
print("Original Data:")
print(data)
print("\nDecimal Scaled Data:")
print(s_data)
