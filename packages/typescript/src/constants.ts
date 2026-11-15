// This module defines project-level constants.

export const EXCLUSION_TEXT : string = "を除く";
export const SUFFIX_OPTIONS : Array<string> = ["丁目", "番地", "番", "号"];
export const PREFECTURE_DIGITS : number = 3;
export const STEP_LABELS = {
  0: "都道府県",
  1: "市区町村",
  2: "町域",
}

// REGEX Constants

export const HAS_PAREN_WITH_VALUES_COMMA = new RegExp("(?=.*、)[（(](.*?)[）)]")
export const NUMBER_RANGE_REGEX = new RegExp("(\d+)\D*[~～〜]\D*(\d+)")
export const STRIP_PAREN_REGEX = new RegExp("[()（）]")
export const MATCH_COMMA_REGEX = new RegExp("[,，､﹑]")
export const MATCH_DASH_REGEX = new RegExp("[-‐‑‒–—―ー－]")
export const MATCH_POSTAL_SYMBOL_REGEX = new RegExp("〒")
export const MATCH_7_DIGITS = new RegExp("^\d{7}$")
export const MATCH_ICHI_EN = new RegExp(".+[市区町村]一円$")