// This module defines project-level constants.

export const EXCLUSION_TEXT : string = "を除く";
export const NOT_LISTED_BELOW_TEXT = "以下に掲載がない場合";
export const BUILDINGS_AFTER_EXCLUDED = "（次のビルを除く）";
export const OTHER = "（その他）";
export const ICHIEN = "一円";
export const SUFFIX_OPTIONS : Array<string> = ["丁目", "番地", "番", "号"];
export const PREFECTURE_DIGITS : number = 3;
export const SPECIAL_NOTES = {
  [BUILDINGS_AFTER_EXCLUDED]: [],
  [OTHER]: [],
  [ICHIEN]: []
};

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
export const SEARCH_FAILED_PREFECTURE = "郵便番号を検索できません。検索ステージ：都道府県";
export const SEARCH_FAILED_CITY = "郵便番号を検索できません。検索ステージ：市区町村";
export const SEARCH_FAILED_TOWN = "郵便番号を検索できません。検索ステージ：町域";
