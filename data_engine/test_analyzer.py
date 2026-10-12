
import unittest

import pandas as pd

from data_engine.analyzer import analyze_dataframe


class TestAnalyzer(unittest.TestCase):
    def test_basic_profile(self):
        df = pd.DataFrame({
            "Name": ["Arun", "Priya", "Arun"],
            "Marks": [85, 92, 85],
        })

        result = analyze_dataframe(df)

        self.assertEqual(result["rows"], 3)
        self.assertEqual(result["columns"], 2)
        self.assertEqual(result["column_names"], ["Name", "Marks"])
        self.assertEqual(result["data_types"]["Name"], "str")
        self.assertEqual(result["missing_values"]["Name"], 0)
        self.assertEqual(result["duplicate_rows"], 1)

    def test_missing_values(self):
        df = pd.DataFrame({
            "Name": ["Arun", None],
            "Marks": [85, 92],
        })

        result = analyze_dataframe(df)

        self.assertEqual(result["missing_values"]["Name"], 1)


if __name__ == "__main__":
    unittest.main()
