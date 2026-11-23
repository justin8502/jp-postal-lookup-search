"""This module defines the PostalAddress class."""

import re
from typing import Any
import warnings

from .types import PostalAddressCustom
from .constants import MATCH_7_DIGITS, SEARCH_FAILED_CITY, SEARCH_FAILED_PREFECTURE, SEARCH_FAILED_TOWN
from .data import postal_code_map, address_map
from .utils import (
  normalize_postal_code,
  search_city,
  search_prefecture,
  search_town,
  split_postal_address
)

class PostalAddress:
  def __init__(
    self,
    value: str = "",
    custom: PostalAddressCustom | None = None
  ):
    self._set_default_values()

    if value:
      self._init_from_value(value)

    # Custom acts as a mask, but does not change the underlying properties.
    # This allows us to manipulate custom independently from the data
    # loaded from address/postal/code
    self._custom = custom

  @property
  def postal_code(self):
    return self._postal_code

  @property
  def kana(self):
    if (self._custom):
      return (
        (self._custom.get("pref_kana") or self.pref_kana) +
        (self._custom.get("city_kana") or self.city_kana) +
        (self._custom.get("town_kana") or self.town_kana) +
        (self._custom.get("street_kana") or self.street_kana) +
        (self._custom.get("building_kana") or self.building_kana)
      )

    return (
      self.pref_kana +
      self.city_kana +
      self.town_kana +
      self.street_kana +
      self.building_kana
    )

  @property
  def address(self) -> str:
    if (self._custom):
      return (
        (self._custom.get("pref") or self.pref) +
        (self._custom.get("city") or self.city) +
        (self._custom.get("town") or self.town) +
        (self._custom.get("street") or self.street) +
        (self._custom.get("building") or self.building)
      )

    return (
      self.pref +
      self.city +
      self.town +
      self.street +
      self.building
    )

  def update(self, values: PostalAddressCustom):
    self.pref = values.get("pref") or self.pref
    self.city = values.get("city") or self.city
    self.town = values.get("town") or self.town
    self.street = values.get("street") or self.street
    self.building = values.get("building") or self.building

    self.pref_kana = values.get("pref_kana") or self.pref_kana
    self.city_kana = values.get("city_kana") or self.city_kana
    self.town_kana = values.get("town_kana") or self.town_kana
    self.street_kana = values.get("street_kana") or self.street_kana
    self.building_kana = values.get("building_kana") or self.building_kana

  def update_custom(self, custom: PostalAddressCustom):
    postal_address_custom_keys = ["pref", "city", "town", "street", "building",
                                  "pref_kana", "city_kana", "town_kana", "street_kana", "building_kana"]

    updated_custom: PostalAddressCustom = {}
    for key in postal_address_custom_keys:
      if key in custom and custom[key]:
        updated_custom[key] = custom[key]
    self._custom = updated_custom

  def set_postal(self, postal_code: str):
    self._postal_code = postal_code

  def reload(self, keep_custom: bool = True):
    normalized_address = normalize_postal_code(self.postal_code)
    if re.fullmatch(MATCH_7_DIGITS, normalized_address):
      self._init_from_postal_code(normalized_address)
    else:
      self._init_from_address(self.pref + self.city + self.town)
    if not keep_custom:
      self.update_custom({})

  def load_from_address(
    self,
    address: str,
    keep_custom: bool = True
  ):
    self._init_from_address(address)
    if not keep_custom:
      self.update_custom({})

  def load_from_postal_code(
    self, 
    postal_code: str,
    keep_custom: bool = True
  ):
    normalized_address = normalize_postal_code(postal_code)
    if not re.fullmatch(MATCH_7_DIGITS, normalized_address): return
    self._init_from_postal_code(normalized_address)
    if not keep_custom:
      self.update({})

  def strict_equal(self, address: "PostalAddress"):

    return (
      self.postal_code == address.postal_code
      and self.pref == address.pref
      and self.city == address.city
      and self.town == address.town
      and self.pref_kana == address.pref_kana
      and self.city_kana == address.city_kana
      and self.town_kana == address.town_kana
    )

  def _set_default_values(self):
    self.set_postal("")

    self.pref = ""
    self.city = ""
    self.town = ""
    self.street = ""
    self.building = ""

    self.pref_kana = ""
    self.city_kana = ""
    self.town_kana = ""
    self.street_kana = ""
    self.building_kana = ""

  def _init_from_value(self, value: str):
    normalized_address = normalize_postal_code(value)
    if re.fullmatch(MATCH_7_DIGITS, normalized_address):
      self._init_from_postal_code(normalized_address)
    else:
      self._init_from_address(value)

  def _init_from_postal_code(self, postal_code: str):
    try:
      self._set_default_values()
      self.set_postal(postal_code)

      prefecture_code, city_town_code = split_postal_address(postal_code)
      prefecture_data = postal_code_map.get(prefecture_code)

      if prefecture_data is None:
        return
      
      raw_pref = prefecture_data.get("prefecture") or ""
      pref, pref_kana = raw_pref.split("|")
      self.pref = pref
      self.pref_kana = pref_kana

      raw_city_town = prefecture_data.get(city_town_code) or ""
      city, town, city_kana, town_kana = raw_city_town.split("|")
      self.city = city
      self.town = town
      self.city_kana = city_kana
      self.town_kana = town_kana

    except (ValueError, AttributeError, TypeError) as e:
      warnings.warn(f"郵便番号の該当住所を検索できません： {postal_code}: {e}", stacklevel=2)

  def _init_from_address(self, address: str):
    query_map = address_map
    i = 0

    i, key, _completed = search_prefecture(i, query_map, address)
    if (i >= len(address) or not key):
      warnings.warn(SEARCH_FAILED_PREFECTURE, stacklevel=2)
      return

    pref_map = query_map[key]

    i, key, _completed = search_city(i, pref_map, address)
    if (i >= len(address) or not key):
      warnings.warn(SEARCH_FAILED_CITY, stacklevel=2)
      return

    city_map = pref_map[key]

    i, key, completed = search_town(i, city_map, address)
    if completed and key:
      self._init_from_postal_code(city_map[key])
      return

    warnings.warn(SEARCH_FAILED_TOWN, stacklevel=2)
    return

  def __eq__(self, address: Any):
    if not isinstance(address, PostalAddress):
      return NotImplemented
    return self.postal_code == address.postal_code
