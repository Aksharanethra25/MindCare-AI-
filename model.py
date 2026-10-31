"""
MindCare AI - Machine Learning Module
Educational demonstration using synthetic wellbeing data.

IMPORTANT:
This model demonstrates sample data patterns only.
It does not diagnose, screen, or predict mental health conditions.
"""

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# 1. Generate Synthetic Wellbeing Dataset
# --------------------------------------------------

def generate_synthetic_data(n_samples=150, random_state=42):
    """Create artificial wellbeing data for demonstration."""

    np.random.seed(random_state)

    data = pd.DataFrame({
        "mood_score": np.random.randint(1, 11, n_samples),
        "energy_score": np.random.randint(1, 11, n_samples),
        "sleep_hours": np.round(
            np.random.uniform(3, 10, n_samples), 1
        ),
        "stress_level": np.random.randint(1, 11, n_samples)
    })

    return data


# --------------------------------------------------
# 2. Prepare Dataset
# --------------------------------------------------

def preprocess_data(data):
    """Scale numerical features for clustering."""

    features = [
        "mood_score",
        "energy_score",
        "sleep_hours",
        "stress_level"
    ]

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[features])

    return scaled_data, scaler


# --------------------------------------------------
# 3. Train K-Means Clustering Model
# --------------------------------------------------

def train_wellbeing_model(data=None, n_clusters=3):
    """
    Train an illustrative K-Means model.

    Returns:
        data: Dataset with cluster assignments
        model: Trained K-Means model
        scaler: Fitted feature scaler
    """

    if data is None:
        data = generate_synthetic_data()

    if n_clusters < 2 or n_clusters > len(data):
        raise ValueError(
            "Number of clusters must be between 2 and dataset size."
        )

    scaled_data, scaler = preprocess_data(data)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    data = data.copy()
    data["cluster"] = model.fit_predict(scaled_data)

    return data, model, scaler


# --------------------------------------------------
# 4. Generate Cluster Summary
# --------------------------------------------------

def get_cluster_summary(data):
    """Calculate average sample values for each cluster."""

    features = [
        "mood_score",
        "energy_score",
        "sleep_hours",
        "stress_level"
    ]

    summary = data.groupby("cluster")[features].mean()

    return summary.round(2)


# --------------------------------------------------
# 5. Run Standalone Demonstration
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print("       MINDCARE AI - ML DEMONSTRATION")
    print("=" * 50)

    dataset = generate_synthetic_data()

    results, model, scaler = train_wellbeing_model(
        dataset,
        n_clusters=3
    )

    print("\nSample Dataset:")
    print(results.head(10))

    print("\nCluster Summary:")
    print(get_cluster_summary(results))

    print("\nNumber of Sample Records:", len(results))
    print("Number of Clusters:", model.n_clusters)

    print("\nML Demonstration Completed Successfully!")

    print("\nNote: These are artificial data patterns,")
    print("not clinical assessments or predictions.")
