import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
import graphviz

# Input Data (Features X, Target y)
X = np.array([
    [2.0, 3.0], [5.1, 4.2], [9.0, 6.5], [4.1, 7.3],
    [8.5, 1.1], [7.2, 2.5], [6.0, 5.5], [3.2, 8.0],
    [1.8, 1.9], [4.8, 3.9]
])
y = np.array([0, 1, 1, 0, 1, 1, 0, 0, 0, 1])

f_names = ['feature1', 'feature2']
c_names = ['Class_0', 'Class_1']

# Split Data
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and Train Classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_tr, y_tr)

# Predict and Evaluate
preds = clf.predict(X_te)
acc = accuracy_score(y_te, preds)

# Export and Visualize Tree
dot_data = export_graphviz(clf, out_file=None,
                           feature_names=f_names,
                           class_names=c_names,
                           filled=True, rounded=True,
                           special_characters=True)

graph = graphviz.Source(dot_data)
fname = "dtree_classifier_viz"

# Output
print(f"Accuracy: {acc:.4f}")
try:
    graph.render(fname, view=False, cleanup=True)
    print(f"Tree visualization saved: {fname}.gv.pdf") # .render often creates PDF by default
except Exception as e:
     print(f"Could not render viz: {e}.")
