import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

X = np.array([
    [2.0, 3.0], [5.1, 4.2], [9.0, 6.5], [4.1, 7.3],
    [8.5, 1.1], [7.2, 2.5], [6.0, 5.5], [3.2, 8.0],
    [1.8, 1.9], [4.8, 3.9], [2.5, 1.5], [7.8, 3.1]
])
y = np.array([0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1])

# Split Data
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and Train Model
model = LogisticRegression(random_state=42)
model.fit(X_tr, y_tr)

# Predict and Evaluate
preds = model.predict(X_te)
acc = accuracy_score(y_te, preds)
report = classification_report(y_te, preds, zero_division=0)

# Output
print(f"Accuracy: {acc:.4f}")
print("\nClassification Report:")
print(report)
