"""This module defines project-level constants."""

from .types import SpecialNotes

EXCLUSION_TEXT = "を除く"
NOT_LISTED_BELOW_TEXT = "以下に掲載がない場合"
BUILDINGS_AFTER_EXCLUDED = "（次のビルを除く）"
OTHER = "（その他）"
ICHIEN = "一円"
SUFFIX_OPTIONS = ["丁目", "番地", "番", "号"]
PREFECTURE_DIGITS = 3
STEP_LABELS = {
  0: "都道府県",
  1: "市区町村",
  2: "町域",
}
SPECIAL_NOTES: SpecialNotes = {
  BUILDINGS_AFTER_EXCLUDED: [],
  OTHER: [],
  ICHIEN: []
}

"""REGEX Constants"""

HAS_PAREN_WITH_VALUES_COMMA = r"(?=.*、)[（(](.*?)[）)]"
NUMBER_RANGE_REGEX = r"(\d+)\D*[~～〜]\D*(\d+)"
STRIP_PAREN_REGEX = r"[()（）]"
MATCH_COMMA_REGEX = r"[,，､﹑]"
MATCH_DASH_REGEX = r"[-‐‑‒–—―ー－]"
MATCH_POSTAL_SYMBOL_REGEX = r"〒"
MATCH_7_DIGITS = r"^\d{7}$"
MATCH_ICHI_EN = r".+[市区町村]一円$"

"""Errors"""

PREFECTURE_NOT_FOUND = "都道府県情報を検索できません。"
CITY_TOWN_NOT_FOUND = "住所情報を検索できません。"
SEARCH_FAILED_PREFECTURE = "郵便番号を検索できません。検索ステージ：都道府県"
SEARCH_FAILED_CITY = "郵便番号を検索できません。検索ステージ：市区町村"
SEARCH_FAILED_TOWN = "郵便番号を検索できません。検索ステージ：町域"
