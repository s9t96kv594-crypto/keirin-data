# -*- coding: utf-8 -*-
"""Conservative repair helpers for historical keirin CSV fields."""
import re

PREFECTURES = {
    "北海道", "青森", "岩手", "宮城", "秋田", "山形", "福島",
    "茨城", "栃木", "群馬", "埼玉", "千葉", "東京", "神奈川",
    "新潟", "富山", "石川", "福井", "山梨", "長野", "岐阜",
    "静岡", "愛知", "三重", "滋賀", "京都", "大阪", "兵庫",
    "奈良", "和歌山", "鳥取", "島根", "岡山", "広島", "山口",
    "徳島", "香川", "愛媛", "高知", "福岡", "佐賀", "長崎",
    "熊本", "大分", "宮崎", "鹿児島", "沖縄",
}


def repair_player_prefecture(player_name, pref):
    """Return (player_name, pref, repaired) without guessing ambiguous rows.

    Known historical defect: the first character of a prefecture was appended
    to player_name and the remaining characters were stored in pref. Repair
    only when the reconstructed value exactly matches a Japanese prefecture.
    """
    name = "" if player_name is None else str(player_name)
    pref_text = "" if pref is None else str(pref).strip()
    if pref_text in PREFECTURES:
        return name, pref_text, False

    m = re.match(r"^(.*?)\\s+([^\\s])$", name.strip())
    if m:
        candidate = m.group(2) + pref_text
        if candidate in PREFECTURES:
            return m.group(1).strip(), candidate, True

    return name, pref_text, False


def repair_prefecture_columns(frame):
    """Return a copy with only provably repairable name/pref pairs corrected."""
    if "player_name" not in frame.columns or "pref" not in frame.columns:
        return frame.copy(), 0

    repaired_pairs = [
        repair_player_prefecture(name, pref)
        for name, pref in zip(frame["player_name"], frame["pref"])
    ]
    result = frame.copy()
    result["player_name"] = [item[0] for item in repaired_pairs]
    result["pref"] = [item[1] for item in repaired_pairs]
    count = sum(1 for item in repaired_pairs if item[2])
    return result, count
