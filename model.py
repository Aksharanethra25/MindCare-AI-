MindCare AI - Machine Learning Module

Purpose:
Demonstrates K-Means clustering using synthetic wellbeing data.

Important:
This is an educational machine learning demonstration.
It does not diagnose, predict, or classify mental health conditions.
"""

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

FEATURE_COLUMNS = [
    "mood_score",
    "energy_score",
    "sleep_hours",
    "stress_level"
]


# --------------------------------------------------
# 2. GENERATE SYNTHETIC WELLBEING DATA
# --------------------------------------------------

def generate_synthetic_data(n_samples=150, random_state=42):
    """
    Generate sample wellbeing data for ML demonstration.

    Returns:
        pandas DataFrame
    """

    if n_samples < 3:
        raise ValueError("n_samples must be at least 3.")

    if n_samples > 100000:
        raise ValueError("n_samples is too large for this demonstration.")

    rng = np.random.default_rng(random_state)

    data = pd.DataFrame({
        "mood_score": rng.integers(1, 11, n_samples),
        "energy_score": rng.integers(1, 11, n_samples),
        "sleep_hours": np.round(
            rng.uniform(3.0, 10.0, n_samples), 1
        ),
        "stress_level": rng.integers(1, 11, n_samples)
    })

    return data


# --------------------------------------------------
# 3. VALIDATE DATA
# --------------------------------------------------

def validate_data(data):
    """
    Check whether the required columns and values exist.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    missing_columns = [
        column for column in FEATURE_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if data.empty:
        raise ValueError("Input data cannot be empty.")

    if data[FEATURE_COLUMNS].isnull().any().any():
        raise ValueError("Input data contains missing values.")

    if not data[FEATURE_COLUMNS].apply(
        lambda column: pd.api.types.is_numeric_dtype(column)
    ).all():
        raise ValueError("All ML features must be numeric.")

    if not np.isfinite(
        data[FEATURE_COLUMNS].to_numpy(dtype=float)
    ).all():
        raise ValueError("Input data contains invalid numeric values.")

    return True


# --------------------------------------------------
# 4. DATA PREPROCESSING
# --------------------------------------------------

def preprocess_data(data):
    """
    Standardize the numerical features.

    Returns:
        Scaled NumPy array
    """

    validate_data(data)

    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(
        data[FEATURE_COLUMNS]
    )

    return scaled_data


# --------------------------------------------------
# 5. TRAIN K-MEANS MODEL
# --------------------------------------------------

def train_wellbeing_model(
    data=None,
    n_clusters=3,
    random_state=42
):
    """
    Train a K-Means clustering model.

    Returns:
        model, scaled_data, scaler
    """

    if data is None:
        data = generate_synthetic_data()

    validate_data(data)

    if not isinstance(n_clusters, int) or isinstance(
        n_clusters, bool
    ):
        raise ValueError("n_clusters must be an integer.")

    if n_clusters < 1 or n_clusters > len(data):
        raise ValueError(
            "n_clusters must be between 1 and the number of rows."
        )

    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(
        data[FEATURE_COLUMNS]
    )

    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )

    model.fit(scaled_data)

    return model, scaled_data, scaler


# --------------------------------------------------
# 6. GENERATE CLUSTER SUMMARY
# --------------------------------------------------

def get_cluster_summary(data):
    """
    Generate a summary of the clusters.

    The input DataFrame must contain a 'cluster' column.
    """

    validate_data(data)

    if "cluster" not in data.columns:
        raise ValueError(
            "Data must contain a 'cluster' column."
        )

    summary = (
        data.groupby("cluster")[FEATURE_COLUMNS]
        .mean()
        .round(2)
    )

    return summary


# --------------------------------------------------
# 7. RUN DEMONSTRATION
# --------------------------------------------------

def run_demo():

    print("\n====================================")
    print("       MINDCARE AI - ML DEMO")
    print("====================================")

    # Generate sample data
    data = generate_synthetic_data()

    print("\nSample Wellbeing Data:")
    print(data.head())

    # Train model
    model, scaled_data, scaler = train_wellbeing_model(
        data=data,
        n_clusters=3
    )

    # Add cluster labels
    data["cluster"] = model.labels_

    # Display cluster summary
    summary = get_cluster_summary(data)

    print("\nCluster Summary:")
    print(summary)

    print("\nNumber of Clusters:", model.n_clusters)
    print("Number of Records:", len(data))

    print("\nML demonstration completed successfully.")


# --------------------------------------------------
# 8. MAIN
# --------------------------------------------------

if __name__ == "__main__":
    run_demo()
