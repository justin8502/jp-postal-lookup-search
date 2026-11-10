from .data import postal_code_map, address_map
from .utils import extract_query_positional_arguments, normalize, split_postal_address, strip_paren
import re

def lookup_address_by_postal_code(postal_code: str) -> str:
  prefecture_code, city_town_code = split_postal_address(postal_code)
  prefecture_data = postal_code_map.get(prefecture_code)

  if prefecture_data is None:
      return "都道府県情報を検索できません。"

  raw_pref = prefecture_data.get("prefecture")
  raw_city_town = prefecture_data.get(city_town_code)

  if raw_pref is None or raw_city_town is None:
    return "住所情報を検索できません。"

  pref, _pref_kana = raw_pref.split("|")
  city, town, _city_kana, _town_kana = raw_city_town.split("|")
  return pref + city + town

def lookup_address_by_postal_code_kana(postal_code: str) -> str:
  prefecture_code, city_town_code = split_postal_address(postal_code)
  prefecture_data = postal_code_map.get(prefecture_code)
  
  if prefecture_data is None:
      return "都道府県情報を検索できません。"

  raw_pref = prefecture_data.get("prefecture")
  raw_city_town = prefecture_data.get(city_town_code)

  if raw_pref is None or raw_city_town is None:
    return "住所情報を検索できません。"

  _pref, pref_kana = raw_pref.split("|")
  _city, _town, city_kana, town_kana = raw_city_town.split("|")
  return pref_kana + city_kana + town_kana

def search_postal_code_by_address(address: str) -> str:
  query_map = address_map.keys()
  # step: 0-prefecture 1-city 2-town
  step = 0
  i = 0

  step_labels = {
    0: "都道府県",
    1: "市区町村",
    2: "町域",
  }

  # Use a sliding window approach + lenient matches
  while i < len(address): 
    special_notes = {
      "（次のビルを除く）": [],
      "（その他）": [],
      "一円": []
    }

    # no entries begin with special characters, so narrow the query.
    matching_first_char_map = [key for key in query_map if key[0] == address[i]]
    for key in matching_first_char_map:
      normalized_query = normalize(address[i:i+len(key)])
      stripped_query = strip_paren(normalized_query)
      normalized_key = normalize(key)
      stripped_key = strip_paren(normalized_key)
      if "（次のビルを除く）" in key:
        special_notes["（次のビルを除く）"] += [key]
      if "（その他）" in key:
        special_notes["（その他）"] += [key]
  
      if step == 2:
        if bool(re.search(r".+[市区町村]一円$", stripped_key)):
          return query_map[key]
        augmented_keys = extract_query_positional_arguments(normalized_key)
        for stripped_key in augmented_keys:
          if stripped_query.startswith(stripped_key) or stripped_key.startswith(stripped_query):
            return query_map[key]
      elif stripped_key.startswith(stripped_query):
        query_map = address_map[key] if step == 0 else query_map[key]
        step += 1
        i += len(key)
        break
    else:
      for note in special_notes:
        for final_key in special_notes[note]:
          normalized_query = normalize(address[i:i+len(final_key)-len(note)])
          stripped_query = strip_paren(normalized_query)
          if normalized_query + note == final_key:
            return query_map[final_key]
      i += 1

  if step == 2:
    # Explicit 一円 match
    if len(query_map) == 1:
      key = next(iter(query_map))

      if re.search(r".+[市区町村]一円$", key):
        return query_map[key]
    return query_map.get("以下に掲載がない場合", "")

  return f"郵便番号を検索できません。検索ステージ：{step_labels[step]}"

# TODO
def create_loc_from_postal():
  return None

# TODO
def create_loc_from_addr():
  return None