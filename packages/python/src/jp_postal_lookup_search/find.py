"""This module implements project-level functions."""

from typing import Dict

from .constants import (
  CITY_TOWN_NOT_FOUND,
  PREFECTURE_NOT_FOUND,
  SEARCH_FAILED_CITY,
  SEARCH_FAILED_PREFECTURE,
  SEARCH_FAILED_TOWN
)
from .types import AddressParts
from .data import postal_code_map, address_map
from .utils import (
  normalize_postal_code,
  search_city,
  search_town,
  split_postal_address,
  search_prefecture,
)

def lookup_address_by_postal_code(postal_code: str) -> str:
  postal_code = normalize_postal_code(postal_code)
  prefecture_code, city_town_code = split_postal_address(postal_code)
  prefecture_data: Dict[str, str] | None = postal_code_map.get(prefecture_code)

  if prefecture_data is None:
      return PREFECTURE_NOT_FOUND

  raw_pref: str | None = prefecture_data.get("prefecture")
  raw_city_town: str | None = prefecture_data.get(city_town_code)

  if raw_pref is None or raw_city_town is None:
    return CITY_TOWN_NOT_FOUND

  pref, _pref_kana = raw_pref.split("|")
  city, town, _city_kana, _town_kana = raw_city_town.split("|")
  return pref + city + town

def lookup_address_parts_by_postal_code(postal_code: str) -> AddressParts:
  postal_code = normalize_postal_code(postal_code)
  address_parts: AddressParts = {
    "pref": "",
    "city": "",
    "town": "",
    "pref_kana": "",
    "city_kana": "",
    "town_kana": ""
  }
  prefecture_code, city_town_code = split_postal_address(postal_code)
  prefecture_data: Dict[str, str] | None = postal_code_map.get(prefecture_code)

  if prefecture_data is None:
    return address_parts

  raw_pref: str | None = prefecture_data.get("prefecture")
  raw_city_town: str | None = prefecture_data.get(city_town_code)

  if raw_pref is None:
    return address_parts

  pref, pref_kana = raw_pref.split("|")
  address_parts["pref"] = pref
  address_parts["pref_kana"] = pref_kana

  if raw_city_town is None:
    return address_parts

  city, town, city_kana, town_kana = raw_city_town.split("|")
  address_parts["city"] = city
  address_parts["city_kana"] = city_kana
  address_parts["town"] = town
  address_parts["town_kana"] = town_kana

  return address_parts

def lookup_address_kana_by_postal_code(postal_code: str) -> str:
  postal_code = normalize_postal_code(postal_code)
  prefecture_code, city_town_code = split_postal_address(postal_code)
  prefecture_data = postal_code_map.get(prefecture_code)
  
  if prefecture_data is None:
      return PREFECTURE_NOT_FOUND

  raw_pref: str | None = prefecture_data.get("prefecture")
  raw_city_town: str | None = prefecture_data.get(city_town_code)

  if raw_pref is None or raw_city_town is None:
    return CITY_TOWN_NOT_FOUND

  _pref, pref_kana = raw_pref.split("|")
  _city, _town, city_kana, town_kana = raw_city_town.split("|")
  return pref_kana + city_kana + town_kana

def search_postal_code_by_address(address: str) -> str:
  query_map = address_map
  i = 0

  i, key, _completed = search_prefecture(i, query_map, address)
  if (i >= len(address) or not key): return SEARCH_FAILED_PREFECTURE

  pref_map = query_map[key]

  i, key, _completed = search_city(i, pref_map, address)
  if (i >= len(address) or not key): return SEARCH_FAILED_CITY

  city_map = pref_map[key]

  i, key, completed = search_town(i, city_map, address)
  if completed and key: return city_map[key]
  return SEARCH_FAILED_TOWN
