from typing import Dict

from .data import postal_code_map, address_map
from .utils import (
  extract_query_positional_arguments,
  normalize_strip_fill,
  normalize_postal_code,
  split_postal_address,
  search_special_notes,
  search_ichien,
  search_ichien_other,
)

def lookup_address_by_postal_code(postal_code: str) -> str:
  postal_code = normalize_postal_code(postal_code)
  prefecture_code, city_town_code = split_postal_address(postal_code)
  prefecture_data: Dict[str, str] | None = postal_code_map.get(prefecture_code)

  if prefecture_data is None:
      return "都道府県情報を検索できません。"

  raw_pref: str | None = prefecture_data.get("prefecture")
  raw_city_town: str | None = prefecture_data.get(city_town_code)

  if raw_pref is None or raw_city_town is None:
    return "住所情報を検索できません。"

  pref, _pref_kana = raw_pref.split("|")
  city, town, _city_kana, _town_kana = raw_city_town.split("|")
  return pref + city + town

def lookup_address_by_postal_code_kana(postal_code: str) -> str:
  postal_code = normalize_postal_code(postal_code)
  prefecture_code, city_town_code = split_postal_address(postal_code)
  prefecture_data: Dict[str, str] = postal_code_map.get(prefecture_code)
  
  if prefecture_data is None:
      return "都道府県情報を検索できません。"

  raw_pref: str | None = prefecture_data.get("prefecture")
  raw_city_town: str | None = prefecture_data.get(city_town_code)

  if raw_pref is None or raw_city_town is None:
    return "住所情報を検索できません。"

  _pref, pref_kana = raw_pref.split("|")
  _city, _town, city_kana, town_kana = raw_city_town.split("|")
  return pref_kana + city_kana + town_kana

def search_postal_code_by_address(address: str) -> str:
  query_map = address_map
  # step: 0-prefecture 1-city 2-town
  step = 0
  i = 0

  step_labels = {
    0: "都道府県",
    1: "市区町村",
    2: "町域",
  }

  special_notes: Dict[str, list[str]] = {
    "（次のビルを除く）": [],
    "（その他）": [],
    "一円": []
  }

  # Use a sliding window approach + lenient matches
  while i < len(address): 
    # no entries begin with special characters, so narrow the query.
    keys_matching_address_first_char: list[str] = [key for key in query_map if key[0] == address[i]]
    for key in keys_matching_address_first_char:
      [
        _normalized_query,
        stripped_query,
        normalized_key,
        stripped_key
      ] = normalize_strip_fill(address[i:i+len(key)], key, special_notes)

      # For town matches, explode number ranges and do fuzzy matching
      # e.g. 宮崎県日南市吾田東（５～１１丁目） -> 宮崎県日南市吾田東５丁目, 宮崎県日南市吾田東６丁目...
      if step == 2:
        if bool(search_ichien(stripped_key)):
          return query_map[key]
        range_selection_expanded_keys = extract_query_positional_arguments(normalized_key)
        for stripped_key in range_selection_expanded_keys:
          if stripped_query.startswith(stripped_key) or stripped_key.startswith(stripped_query):
            return query_map[key]
      elif stripped_key.startswith(stripped_query):
        query_map = query_map[key]
        step += 1
        i += len(key)
        break
    else:
      special_note = search_special_notes(address, i, special_notes, query_map)
      if special_note: return special_note
      i += 1

  ichien_other = search_ichien_other(step, query_map)
  if ichien_other: return ichien_other

  return f"郵便番号を検索できません。検索ステージ：{step_labels[step]}"