# frozen_string_literal: true

# This module defines project-level constants.
module JpPostalLookupSearch
  module Constants
    EXCLUSION_TEXT = "を除く"
    NOT_LISTED_BELOW_TEXT = "以下に掲載がない場合"
    BUILDINGS_AFTER_EXCLUDED = "（次のビルを除く）"
    OTHER = "（その他）"
    ICHIEN = "一円"
    SUFFIX_OPTIONS = %w[丁目 番地 番 号"].freeze
    PREFECTURE_DIGITS = 3
    SPECIAL_NOTES = {
      BUILDINGS_AFTER_EXCLUDED: [],
      OTHER: [],
      ICHIEN: []
    }.freeze

    # REGEX Constants

    HAS_PAREN_WITH_VALUES_COMMA = /(?=.*、)[（(](.*?)[）)]/
    NUMBER_RANGE_REGEX = /(\d+)\D*[~～〜]\D*(\d+)/
    STRIP_PAREN_REGEX = /[()（）]/
    MATCH_COMMA_REGEX = /[,，､﹑]/
    MATCH_DASH_REGEX = /[-‐‑‒–—―ー－]/
    MATCH_POSTAL_SYMBOL_REGEX = /〒/
    MATCH_7_DIGITS = /^\d{7}$/
    MATCH_ICHI_EN = /.+[市区町村]一円$/

    # Errors

    PREFECTURE_NOT_FOUND = "都道府県情報を検索できません。"
    CITY_TOWN_NOT_FOUND = "住所情報を検索できません。"
    SEARCH_FAILED_PREFECTURE = "郵便番号を検索できません。検索ステージ：都道府県"
    SEARCH_FAILED_CITY = "郵便番号を検索できません。検索ステージ：市区町村"
    SEARCH_FAILED_TOWN = "郵便番号を検索できません。検索ステージ：町域"
  end

  include Constants
end
