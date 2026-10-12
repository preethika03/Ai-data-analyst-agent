
import tempfile
import unittest
from pathlib import Path

from data_engine.loader import load_dataset


class TestDataLoader(unittest.TestCase):
    def test_load_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "sample.csv"
            file_path.write_text(
                "Name,Marks\nArun,85\nPriya,92\n",
                encoding="utf-8",
            )

            df = load_dataset(str(file_path))

            self.assertEqual(len(df), 2)
            self.assertEqual(list(df.columns), ["Name", "Marks"])
            self.assertEqual(df.iloc[0]["Name"], "Arun")

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing.csv"

            with self.assertRaises(FileNotFoundError):
                load_dataset(str(file_path))

    def test_unsupported_file_type(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "sample.txt"
            file_path.write_text("example", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_dataset(str(file_path))


if __name__ == "__main__":
    unittest.main()
