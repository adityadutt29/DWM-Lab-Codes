import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Input Data
data = np.array([
    [10.0, 200.0, -5.0],
    [15.0, 180.0, 0.0],
    [5.0, 250.0, 10.0],
    [12.0, 210.0, -2.0]
], dtype=float)

# Scaler Initialization
sclr = MinMaxScaler()

# Fit and Transform
s_data = sclr.fit_transform(data)

# Output
print("Original Data:")
print(data)
print("\nMin-Max Scaled Data:")
print(s_data)
