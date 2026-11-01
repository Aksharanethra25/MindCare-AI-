"""
MindCare AI - Machine Learning Unit Tests

Run using:
python -m unittest test_model.py
"""

import unittest
import pandas as pd

from model import (
    generate_synthetic_data,
    validate_data,
    preprocess_data,
    train_wellbeing_model,
    get_cluster_summary,
    FEATURE_COLUMNS
)


class TestMindCareModel(unittest.TestCase):

    def setUp(self):
        self.data = generate_synthetic_data(
            n_samples=100,
            random_state=42
        )

    def test_data_generation(self):
        self.assertIsInstance(self.data, pd.DataFrame)
        self.assertEqual(len(self.data), 100)

    def test_required_columns(self):
        for column in FEATURE_COLUMNS:
            self.assertIn(column, self.data.columns)

    def test_data_ranges(self):
        self.assertTrue(
            self.data["mood_score"].between(1, 10).all()
        )
        self.assertTrue(
            self.data["energy_score"].between(1, 10).all()
        )
        self.assertTrue(
            self.data["sleep_hours"].between(3, 10).all()
        )
        self.assertTrue(
            self.data["stress_level"].between(1, 10).all()
        )

    def test_data_validation(self):
        self.assertTrue(validate_data(self.data))

    def test_preprocessing(self):
        scaled = preprocess_data(self.data)

        self.assertEqual(scaled.shape, (100, 4))

    def test_model_training(self):
        model, scaled, scaler = train_wellbeing_model(
            self.data,
            n_clusters=3
        )

        self.assertEqual(model.n_clusters, 3)
        self.assertEqual(scaled.shape, (100, 4))
        self.assertIsNotNone(scaler)

    def test_cluster_labels(self):
        model, scaled, scaler = train_wellbeing_model(
            self.data,
            n_clusters=3
        )

        self.assertEqual(len(model.labels_), 100)
        self.assertTrue(
            set(model.labels_).issubset({0, 1, 2})
        )

    def test_cluster_summary(self):
        model, scaled, scaler = train_wellbeing_model(
            self.data,
            n_clusters=3
        )

        result = self.data.copy()
        result["cluster"] = model.labels_

        summary = get_cluster_summary(result)

        self.assertIsInstance(summary, pd.DataFrame)
        self.assertEqual(len(summary.columns), 4)

    def test_missing_column(self):
        invalid_data = self.data.drop(columns=["mood_score"])

        with self.assertRaises(ValueError):
            validate_data(invalid_data)

    def test_empty_data(self):
        empty_data = self.data.iloc[0:0]

        with self.assertRaises(ValueError):
            validate_data(empty_data)

    def test_invalid_cluster_count(self):
        with self.assertRaises(ValueError):
            train_wellbeing_model(
                self.data,
                n_clusters=0
            )


if __name__ == "__main__":
    unittest.main()
