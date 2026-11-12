import re
import warnings
from typing import Dict, TypedDict
from .constants import MATCH_7_DIGITS
from .data import postal_code_map, address_map
from .utils import (
  extract_query_positional_arguments,
  normalize_strip_fill,
  normalize_postal_code,
  search_ichien,
  search_ichien_other,
  search_special_notes,
  split_postal_address
)

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

    print(value)
    if value:
      self._init_from_value(value)

    self._custom = custom or {}

  @property
  def postal_code(self):
    return self._postal_code

  @property
  def kana(self):
    return (
      (self._custom.get("pref_kana") or self.pref_kana or "") +
      (self._custom.get("city_kana") or self.city_kana or "") +
      (self._custom.get("town_kana") or self.town_kana or "") +
      (self._custom.get("street_kana") or self.street_kana or "") +
      (self._custom.get("building_kana") or self.building_kana or "")
    )

  @property
  def address(self):
    return (
      (self._custom.get("pref") or self.pref or "") +
      (self._custom.get("city") or self.city or "") +
      (self._custom.get("town") or self.town or "") +
      (self._custom.get("street") or self.street or "") +
      (self._custom.get("building") or self.building or "")
    )

  def update(self, custom: PostalAddressCustom):
    postal_address_custom_keys = ["pref", "city", "town", "street", "building"
                                  "pref_kana", "city_kana", "town_kana", "street_kana", "building_kana"]

    updated_custom = {}
    for key in postal_address_custom_keys:
      if key in custom and custom[key]:
        updated_custom[key] = custom[key]
    self._custom = updated_custom

  def set_postal(self, postal_code):
    self._postal_code = postal_code

  def reload(self, keep_custom: bool = True):
    if re.fullmatch(MATCH_7_DIGITS, self.postal_code):
      self._init_from_postal_code(self.postal_code)
    else:
      self._init_from_address(self.pref + self.city + self.town)
    if not keep_custom:
      self.update({})

  def load_from_address(
    self,
    address: str,
    keep_custom: bool = True
  ):
    self._init_from_address(address)
    if not keep_custom:
      self.update({})

  def load_from_postal_code(
    self, 
    postal_code: str,
    keep_custom: bool = True
  ):
    if not re.fullmatch(MATCH_7_DIGITS, postal_code): return
    self._init_from_postal_code(postal_code)
    if not keep_custom:
      self.update({})

  def strict_equal(self, address):
    if not isinstance(address, PostalAddress):
      return False

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
      warnings.warn(f"郵便番号の該当住所を検索できません： {postal_code}: {e}", stacklevel=2)

  def _init_from_address(self, address: str):
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
            self._process_step(step, key)
            self._init_from_postal_code(query_map[key])
            return
          range_selection_expanded_keys = extract_query_positional_arguments(normalized_key)
          for stripped_key in range_selection_expanded_keys:
            if stripped_query.startswith(stripped_key) or stripped_key.startswith(stripped_query):
              self._init_from_postal_code(query_map[key])
              return
        elif stripped_key.startswith(stripped_query):
          query_map = query_map[key]
          self._process_step(step, key)
          step += 1
          i += len(key)
          break
      else:
        special_note = search_special_notes(address, i, special_notes, query_map)
        if special_note:
          self._init_from_postal_code(query_map[key])
          return
        i += 1

    ichien_other = search_ichien_other(step, query_map)
    if ichien_other:
      self._init_from_postal_code(query_map[key])
      return

    warnings.warn(f"郵便番号を検索できません。検索ステージ：{step_labels[step]}", stacklevel=2)

  def _process_step(self, step: int, value: str):
    # Load Partials
    match step:
      case 0:
        self.pref = value
      case 1:
        self.city = value
      case 2:
        self.town = value

  def __eq__(self, address):
    if not isinstance(address, PostalAddress):
      return NotImplemented
    return self.postal_code == address.postal_code