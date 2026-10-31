"""Automated tests for the MindCare AI ML module."""

import unittest

from model import (
    generate_synthetic_data,
    preprocess_data,
    train_wellbeing_model,
    get_cluster_summary
)


class TestMindCareModel(unittest.TestCase):

    def setUp(self):
        self.data = generate_synthetic_data(
            n_samples=100,
            random_state=42
        )

    def test_dataset_generation(self):
        self.assertEqual(len(self.data), 100)
        self.assertIn("mood_score", self.data.columns)
        self.assertIn("energy_score", self.data.columns)
        self.assertIn("sleep_hours", self.data.columns)
        self.assertIn("stress_level", self.data.columns)

    def test_dataset_values(self):
        self.assertTrue(
            self.data["mood_score"].between(1, 10).all()
        )
        self.assertTrue(
            self.data["energy_score"].between(1, 10).all()
        )
        self.assertTrue(
            self.data["stress_level"].between(1, 10).all()
        )

    def test_preprocessing(self):
        scaled_data, scaler = preprocess_data(self.data)

        self.assertEqual(scaled_data.shape, (100, 4))
        self.assertIsNotNone(scaler)

    def test_model_training(self):
        results, model, scaler = train_wellbeing_model(
            self.data,
            n_clusters=3
        )

        self.assertEqual(len(results), 100)
        self.assertIn("cluster", results.columns)
        self.assertEqual(model.n_clusters, 3)

    def test_cluster_summary(self):
        results, _, _ = train_wellbeing_model(self.data)
        summary = get_cluster_summary(results)

        self.assertEqual(len(summary.columns), 4)
        self.assertGreaterEqual(len(summary), 1)


if __name__ == "__main__":
    unittest.main()
