"""This module handles loading the prebuilt json files."""

import json
from importlib.resources import files
from typing import cast

from .types import AddressMap, PostalCodeMap

def _as_dict(data: object) -> dict[object, object]:
  if not isinstance(data, dict):
    raise ValueError("Expected a dictionary")

  return cast(dict[object, object], data)

def validate_address_map(data: object) -> AddressMap:
  result = _as_dict(data)

  for pref, cities in result.items():
    if not isinstance(pref, str):
      raise ValueError(f"Invalid prefecture: {pref}")

    for city, towns in _as_dict(cities).items():
      if not isinstance(city, str):
        raise ValueError(f"Invalid city: {city}")

      for town, postal_code in _as_dict(towns).items():
        if not isinstance(town, str) or not isinstance(postal_code, str):
          raise ValueError(f"Invalid town: {town}")

  return cast(AddressMap, result)


def validate_postal_code_map(data: object) -> PostalCodeMap:
  result = _as_dict(data)

  for pref_code, city_town_code in result.items():
    if not isinstance(pref_code, str):
      raise ValueError(f"Invalid prefix: {pref_code}")

    entries = _as_dict(city_town_code)

    if not isinstance(entries.get("prefecture"), str):
      raise ValueError(f"Missing prefecture: {pref_code}")

    if not all(
      isinstance(key, str) and isinstance(value, str)
      for key, value in entries.items()
    ):
      raise ValueError(f"Invalid entries: {pref_code}")

  return cast(PostalCodeMap, result)

postal_code_map: PostalCodeMap = validate_postal_code_map(json.loads(
  files(__package__).joinpath("data/postal_code_lookup.json").read_text(encoding="utf-8")
))

address_map: AddressMap = validate_address_map(json.loads(
  files(__package__).joinpath("data/address_lookup.json").read_text(encoding="utf-8")
))