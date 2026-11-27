import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from player_identity import parse_player_identity


class PlayerIdentityTests(unittest.TestCase):
    def test_prefecture_with_internal_space(self):
        self.assertEqual(
            parse_player_identity("中村 美千隆  兵 庫/50/80"),
            ("中村 美千隆", "兵庫", "50", "80"),
        )

    def test_normal_prefecture(self):
        self.assertEqual(
            parse_player_identity("外崎 一成  北海道/37/94"),
            ("外崎 一成", "北海道", "37", "94"),
        )

    def test_three_character_prefecture(self):
        self.assertEqual(
            parse_player_identity("選手名  神 奈 川/42/100"),
            ("選手名", "神奈川", "42", "100"),
        )

    def test_unmatched_value_is_not_guessed(self):
        self.assertEqual(
            parse_player_identity("選手名だけ"),
            ("選手名だけ", "", "", ""),
        )


if __name__ == "__main__":
    unittest.main()
