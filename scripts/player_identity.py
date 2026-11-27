def parse_player_identity(raw_name):
    """Parse player name, prefecture, age and term from K-Dreams text.

    pandas.read_html can separate characters inside a prefecture, e.g.
    '兵 庫/50/80'. This parser requires 2-4 prefecture characters and
    removes whitespace inside that field.
    """
    raw = str(raw_name).strip()
    m = re.match(r"^(.*?)\s+((?:[^\s/]\s*){2,4})/(\d+)/(\d+)\s*$", raw)
    if m:
        return (m.group(1).strip(), re.sub(r"\s+", "", m.group(2)), m.group(3), m.group(4))
    m = re.match(r"(.+?)\s+(\S+)/(\d+)/(\d+)", raw)
    if m:
        return m.group(1).strip(), m.group(2), m.group(3), m.group(4)
    return raw, "", "", ""
