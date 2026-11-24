"""This module defines custom types."""

from typing import NamedTuple, TypedDict, TypeAlias

TownMap: TypeAlias = dict[str, str]
CityMap: TypeAlias = dict[str, TownMap]
PrefMap: TypeAlias = dict[str, CityMap]
AddressMap: TypeAlias = PrefMap
PrefCodeMap: TypeAlias = dict[str, str]
PostalCodeMap: TypeAlias = dict[str, PrefCodeMap]

class NormalizedAddress(NamedTuple):
  normalized_query: str
  stripped_query: str
  normalized_key: str
  stripped_key: str

class AddressParts(TypedDict):
  pref: str
  city: str
  town: str

  pref_kana: str
  city_kana: str
  town_kana: str

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

SpecialNotes: TypeAlias = dict[str, list[str]]

class SearchReturn(NamedTuple):
  i: int
  key: str | None
  completed: bool
