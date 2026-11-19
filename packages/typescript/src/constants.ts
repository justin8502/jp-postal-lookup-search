// This module defines project-level constants.

export const EXCLUSION_TEXT : string = "を除く";
export const SUFFIX_OPTIONS : Array<string> = ["丁目", "番地", "番", "号"];
export const PREFECTURE_DIGITS : number = 3;
export const STEP_LABELS: {[key: number]: string} = {
  0: "都道府県",
  1: "市区町村",
  2: "町域",
}

// REGEX Constants

export const HAS_PAREN_WITH_VALUES_COMMA = /(?=.*、)[（(](.*?)[）)]/;
export const NUMBER_RANGE_REGEX = /(\d+)\D*[~～〜]\D*(\d+)/;
export const STRIP_PAREN_REGEX = /[()（）]/g;
export const MATCH_COMMA_REGEX = /[,，､﹑、]/;
export const MATCH_DASH_REGEX = /[-‐‑‒–—―ー－]/g;
export const MATCH_POSTAL_SYMBOL_REGEX = /〒/;
export const MATCH_7_DIGITS = /^\d{7}$/;
export const MATCH_ICHI_EN = /.+[市区町村]一円$/;

// Errors

export const PREFECTURE_NOT_FOUND = "都道府県情報を検索できません。";
export const CITY_TOWN_NOT_FOUND = "住所情報を検索できません。";
