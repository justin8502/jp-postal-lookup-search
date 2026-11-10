from .data import postal_code_map, address_map
from .util import extract_query_positional_arguments, normalize, split_postal_address, strip_paren
import re

def lookup_address_by_postal_code(postal_code: str) -> str:
  prefecture_code, city_town_code = split_postal_address(postal_code)
  raw_pref = postal_code_map[prefecture_code]["prefecture"]
  raw_city_town = postal_code_map[prefecture_code][city_town_code]

  pref, _pref_kana = raw_pref.split("|")
  city, town, _city_kana, _town_kana = raw_city_town.split("|")
  return pref + city + town

def lookup_address_by_postal_code_kana(postal_code: str) -> str:
  prefecture_code, city_town_code = split_postal_address(postal_code)
  raw_pref = postal_code_map[prefecture_code]["prefecture"]
  raw_city_town = postal_code_map[prefecture_code][city_town_code]

  _pref, pref_kana = raw_pref.split("|")
  _city, _town, city_kana, town_kana = raw_city_town.split("|")
  return pref_kana + city_kana + town_kana

def search_postal_code_by_address(address: str) -> str:
  query_map = address_map.keys()
  # step: 0-prefecture 1-city 2-town
  step = 0
  i = 0

  # Use a sliding window approach + lenient matches
  while i < len(address): 
    final_check = {
      "（次のビルを除く）": [],
      "（その他）": [],
      "一円": []
    }
    for key in query_map:
      normalized_query = normalize(address[i:i+len(key)])
      stripped_query = strip_paren(normalized_query)
      normalized_key = normalize(key)
      stripped_key = strip_paren(normalized_key)
      if "（次のビルを除く）" in key:
        final_check["（次のビルを除く）"] += [key]
      if "（その他）" in key:
        final_check["（その他）"] += [key]
  
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
      for suffix_type in final_check:
        for final_key in final_check[suffix_type]:
          normalized_query = normalize(address[i:i+len(final_key)-len(suffix_type)])
          stripped_query = strip_paren(normalized_query)
          if normalized_query + suffix_type == final_key:
            return query_map[final_key]
      i += 1

  if step == 2:
    # Explicit 一円 match
    if len(query_map) == 1:
      key = next(iter(query_map))

      if re.search(r".+[市区町村]一円$", key):
        return query_map[key]
    return query_map.get("以下に掲載がない場合", "")

  return ""

# TODO
def create_loc_from_postal():
  return None

# TODO
def create_loc_from_addr():
  return None