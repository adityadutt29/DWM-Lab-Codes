import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# Input Data
X = np.array([
    [2.0, 3.0, 1.0], [5.1, 4.2, 0.5], [9.0, 6.5, 2.0], [4.1, 7.3, 1.5],
    [8.5, 1.1, 0.2], [7.2, 2.5, 0.8], [6.0, 5.5, 1.2], [3.2, 8.0, 1.8],
    [1.8, 1.9, 0.4], [4.8, 3.9, 0.9], [2.5, 1.5, 0.1], [7.8, 3.1, 0.7]
])
y = np.array([0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1])

# Split Data
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and Train Model
model = GaussianNB()
model.fit(X_tr, y_tr)

# Predict and Evaluate
preds = model.predict(X_te)
acc = accuracy_score(y_te, preds)
report = classification_report(y_te, preds, zero_division=0)

# Output
print(f"Accuracy: {acc:.4f}")
print("\nClassification Report:")
print(report)
