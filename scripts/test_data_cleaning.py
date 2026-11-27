import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_cleaning import repair_player_prefecture


class PrefectureRepairTests(unittest.TestCase):
    def test_split_hyogo(self):
        self.assertEqual(
            repair_player_prefecture("中村 美千隆  兵", "庫"),
            ("中村 美千隆", "兵庫", True),
        )

    def test_split_okayama(self):
        self.assertEqual(
            repair_player_prefecture("櫻井 太士  岡", "山"),
            ("櫻井 太士", "岡山", True),
        )

    def test_existing_full_prefecture_unchanged(self):
        self.assertEqual(
            repair_player_prefecture("外崎 一成", "北海道"),
            ("外崎 一成", "北海道", False),
        )

    def test_ambiguous_row_not_guessed(self):
        self.assertEqual(
            repair_player_prefecture("選手名", "不明"),
            ("選手名", "不明", False),
        )


if __name__ == "__main__":
    unittest.main()
