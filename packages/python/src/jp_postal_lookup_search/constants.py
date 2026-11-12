EXCLUSION_TEXT = "を除く"
SUFFIX_OPTIONS = ["丁目", "番地", "番", "号"]
PREFECTURE_DIGITS = 3

HAS_PAREN_WITH_VALUES_COMMA = r"(?=.*、)[（(](.*?)[）)]"
NUMBER_RANGE_REGEX = r"(\d+)\D*[~～〜]\D*(\d+)"
STRIP_PAREN_REGEX = r"[()（）]"
MATCH_COMMA_REGEX = r"[,，､﹑]"
MATCH_DASH_REGEX = r"[-‐‑‒–—―ー－]"
MATCH_POSTAL_SYMBOL_REGEX = r"〒"
MATCH_7_DIGITS = r"^\d{7}$"
MATCH_ICHI_EN = r".+[市区町村]一円$"