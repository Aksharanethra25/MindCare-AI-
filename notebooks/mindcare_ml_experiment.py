"""
MindCare AI - Machine Learning Experiment
Domain: Python and Machine Learning
"""

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# Load dataset
data = pd.read_csv("data/mindcare_wellbeing_data.csv")

print("MindCare AI - ML Experiment")
print(data.head())


# Select features
features = [
    "mood_score",
    "energy_score",
    "sleep_hours",
    "stress_level"
]

X = data[features]


# Data preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# K-Means clustering
model = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

data["cluster"] = model.fit_predict(X_scaled)


# Cluster summary
print("\nCluster Summary:")
print(data.groupby("cluster")[features].mean())


# Visualization
plt.figure(figsize=(8, 5))

plt.scatter(
    data["mood_score"],
    data["stress_level"],
    c=data["cluster"]
)

plt.xlabel("Mood Score")
plt.ylabel("Stress Level")
plt.title("MindCare AI - K-Means Clustering")

plt.show()
