from .data import postal_code_map, address_map

def split_postal_address(addr: str) -> tuple[str, str]:
  return addr[0:3], addr[3:]


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
  step = "pref"
  i = 0

  # Use a sliding window approach + lenient matches
  while i < len(address):
    if step == "pref":
      query_pref = address[i:i+3]
      if query_pref in query_map:
        step = "city"
        query_map = address_map[query_pref]
        i += len(query_pref)
      else:
        i += 1
    elif step == "city":
      for city in query_map:
        query_city = address[i:i+len(city)]
        if query_city == city:
          step = "town"
          query_map = query_map[city]
          i += len(city)
          break
      else:
        i += 1
    elif step == "town":
      for town in query_map:
        query_town = address[i:]
        if town.startswith(query_town):
          return query_map[town]
      i += 1

  if step == "town":
    return query_map.get("以下に掲載がない場合", "")
  return ""

# TODO
def create_loc_from_postal():
  return None

# TODO
def create_loc_from_addr():
  return None