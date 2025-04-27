import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# Generate Sample Data
n_samples = 150
n_features = 2
n_clusters = 3
random_state = 42

X, _ = make_blobs(n_samples=n_samples,
                  n_features=n_features,
                  centers=n_clusters,
                  cluster_std=1.0,
                  random_state=random_state)

# Initialize and Fit K-Means
kmeans = KMeans(n_clusters=n_clusters, n_init='auto', random_state=random_state)
kmeans.fit(X)

# Get Labels and Centers
labels = kmeans.labels_
centers = kmeans.cluster_centers_

# Visualization
plt.figure(figsize=(8, 6))

colors = plt.cm.viridis(np.linspace(0, 1, n_clusters))

for i in range(n_clusters):
    cluster_points = X[labels == i]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1],
                s=50, c=[colors[i]], label=f'Cluster {i}')

plt.scatter(centers[:, 0], centers[:, 1], s=200, c='red', marker='X', label='Centroids')

plt.title('K-Means Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.grid(True)
plt.show()

print("Cluster Centers:")
print(centers)
