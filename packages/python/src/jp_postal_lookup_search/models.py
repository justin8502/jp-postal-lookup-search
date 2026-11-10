from jp_postal_lookup_search.find import (
  lookup_address_by_postal_code,
  lookup_address_by_postal_code_kana,
  search_postal_code_by_address,
)
from .data import postal_code_map, address_map
from .utils import split_postal_address

# Wrapper model may eventually belong here.

class PostalAddress:
  def __init__(self, postal_code=None, overrides=None):
    overrides = overrides or {}
    self.postal_code = postal_code

    prefecture_code, city_town_code = split_postal_address(postal_code)
    prefecture_data = postal_code_map.get(prefecture_code)

    raw_pref = prefecture_data.get("prefecture")
    raw_city_town = prefecture_data.get(city_town_code)

    pref, pref_kana = raw_pref.split("|")
    city, town, city_kana, town_kana = raw_city_town.split("|")
    self.pref = overrides.get("pref") or pref
    self.city = overrides.get("city") or city
    self.town = overrides.get("town") or town
    self.street = overrides.get("street")
    self.building = overrides.get("building")

    self.pref_kana = overrides.get("pref_kana") or pref_kana
    self.city_kana = overrides.get("city_kana") or city_kana
    self.town_kana = overrides.get("town_kana") or town_kana
    self.street_kana = overrides.get("street_kana") or city_kana
    self.building_kana = overrides.get("building_kana") or town_kana
  
  @property
  def postal_code(self):
    return self._postal_code

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

  def kana(self):
    return (
      self.pref_kana +
      self.city_kana +
      self.town_kana +
      self.street_kana +
      self.building_kana
    )

  def set_postal(self, postal_code, preserve_overrides=False):
    self.postal_code = postal_code