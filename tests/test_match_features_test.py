import unittest
from gammaspotter.match_features import MatchFeatures


class TestMatchFeatures(unittest.TestCase):
    def test_matcher(self):
        mf = MatchFeatures()
        found_energy_sigma_list = [[1475.5, 15], [511, 5], [200, 20]]
        energy_list = [
            ["Na-22", 1274.5],
            ["Cs-137", 661.64],
            ["Ba-133", 356],
            ["Co-60", 1173.2],
            ["Co-60", 1332.5],
            ["K-40", 1460],
        ]
        expected_output = [
            [1, "K-40", 30.14479331380494],
            [1, "Co-60", 1.5231238296442572e-19],
            [1, "Na-22", 6.04631547189045e-39],
            [1, "Co-60", 2.5158933893050456e-88],
            [1, "Cs-137", 0.0],
            [1, "Ba-133", 0.0],
            [2, "Cs-137", 2.083181951639746e-197],
            [2, "Ba-133", 5.390500162401e-209],
            [2, "Na-22", 0.0],
            [2, "Co-60", 0.0],
            [2, "Co-60", 0.0],
            [2, "K-40", 0.0],
            [3, "Ba-133", 6.190717543917401e-13],
            [3, "Cs-137", 7.02142579924698e-116],
            [3, "Na-22", 0.0],
            [3, "Co-60", 0.0],
            [3, "Co-60", 0.0],
            [3, "K-40", 0.0],
        ]
        self.assertEqual(
            mf.matcher(found_energy_sigma_list, energy_list), expected_output
        )


if __name__ == "__main__":
    unittest.main()
