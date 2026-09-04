import unittest

from collatz_core import (
    binary_features,
    compare_mersenne_cohort,
    l_harbor,
    l_harbor_binary,
    l_harbor_rows,
    secondary_harbor_member,
    trajectory,
)


class CanonicalMetricsTests(unittest.TestCase):
    def test_l_harbor_identity_and_binary_form(self):
        for k in range(1, 8):
            n = l_harbor(k)
            self.assertEqual(3 * n + 1, 2 ** (2 * k))
            self.assertEqual(format(n, "b"), l_harbor_binary(k))

    def test_l_harbor_step_conventions(self):
        metrics = trajectory(l_harbor(2))
        self.assertEqual(metrics.first_power_of_two_step, 1)
        self.assertEqual(metrics.first_power_of_two_value, 16)
        self.assertEqual(metrics.total_stopping_time, 5)
        self.assertEqual(metrics.sequence_length, 6)

    def test_secondary_harbor_is_exact_not_finite(self):
        self.assertTrue(secondary_harbor_member(5 * 2**100, 5))
        self.assertTrue(secondary_harbor_member(3 * 2**20, 3))
        self.assertFalse(secondary_harbor_member(7, 5))

    def test_metrics_distinguish_bounded_runs(self):
        metrics = trajectory(27, max_steps=0)
        self.assertFalse(metrics.converged)
        self.assertIsNone(metrics.total_stopping_time)
        self.assertEqual(metrics.termination, "max_steps")

    def test_binary_features_are_reproducible(self):
        features = binary_features(85)
        self.assertEqual(features["binary"], "1010101")
        self.assertEqual(features["v2"], 0)
        self.assertEqual(features["has_101"], 1)
        self.assertEqual(features["has_11"], 0)
        self.assertEqual(features["alternating_violations"], 0)


class CohortTests(unittest.TestCase):
    def test_mersenne_cohort_is_exhaustive(self):
        rows = compare_mersenne_cohort(3)
        self.assertEqual([row["start"] for row in rows], [4, 5, 6, 7])
        self.assertEqual(rows[-1]["binary"], "111")

    def test_l_family_rows_include_expected_conventions(self):
        rows = list(l_harbor_rows(4))
        self.assertEqual(
            [row["total_stopping_time"] for row in rows],
            [3, 5, 7, 9],
        )
        self.assertTrue(all(
            row["sequence_length"] == row["expected_sequence_length"]
            for row in rows
        ))


if __name__ == "__main__":
    unittest.main()
