import re
import warnings
from typing import TypedDict
from jp_postal_lookup_search.find import (
  lookup_address_by_postal_code,
  lookup_address_by_postal_code_kana,
  search_postal_code_by_address,
)
from .constants import MATCH_7_DIGIS
from .data import postal_code_map, address_map
from .utils import split_postal_address

class PostalAddressCustom(TypedDict, total=False):
  pref: str
  city: str
  town: str
  street: str
  building: str

  pref_kana: str
  city_kana: str
  town_kana: str
  street_kana: str
  building_kana: str

class PostalAddress:
  def __init__(
    self,
    value: str = "",
    custom: PostalAddressCustom | None = None
  ):
    self._set_default_values()

    if value:
      self._init_from_value(value)

    self._custom = custom or {}
    self._replace_with_custom(custom or {})

  def _init_from_value(self, value: str):
    if re.fullmatch(MATCH_7_DIGIS, value):
      self._init_from_postal_code(value)
    else:
      self._init_from_address(value)

  @property
  def postal_code(self):
    return self._postal_code

  def set_postal(self, postal_code, preserve_custom=False):
    self._postal_code = postal_code

  def __eq__(self, addr):
    if not isinstance(addr, PostalAddress):
      return NotImplemented
    return self.postal_code == addr.postal_code

  def strict_equal(self, addr):
    if not isinstance(addr, PostalAddress):
      return False

    return (
      self.postal_code == addr.postal_code
      and self.pref == addr.pref
      and self.city == addr.city
      and self.town == addr.town
      and self.pref_kana == addr.pref_kana
      and self.city_kana == addr.city_kana
      and self.town_kana == addr.town_kana
    )

  @property
  def kana(self):
    return (
      (self.pref_kana or "") +
      (self.city_kana or "") +
      (self.town_kana or "") +
      (self.street_kana or "") +
      (self.building_kana or "")
    )

  @property
  def addr(self):
    return (
      (self.pref or "") +
      (self.city or "") +
      (self.town or "") +
      (self.street or "") +
      (self.building or "")
    )

  def reload(self):
    self._init_from_value(self.postal_code)
    self._replace_with_custom(self._custom)

  def reload_from_address(self):
    print("TODO")

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

  def _init_from_postal_code(self, postal_code: str):
    try:
      self._set_default_values()
      self.set_postal(postal_code)

      prefecture_code, city_town_code = split_postal_address(postal_code)
      prefecture_data = postal_code_map.get(prefecture_code)

      raw_pref = prefecture_data.get("prefecture")
      pref, pref_kana = raw_pref.split("|")
      self.pref = pref
      self.pref_kana = pref_kana

      raw_city_town = prefecture_data.get(city_town_code)
      city, town, city_kana, town_kana = raw_city_town.split("|")
      self.city = city
      self.town = town
      self.city_kana = city_kana
      self.town_kana = town_kana

    except (ValueError, AttributeError, TypeError) as e:
      warnings.warn(f"Failed to resolve postal code {postal_code}: {e}", stacklevel=2)

  def _init_from_address(self):
    print("TODO")

  def _replace_with_custom(self, custom: PostalAddressCustom):
    for key, value in custom.items():
      if value:
        setattr(self, key, value)