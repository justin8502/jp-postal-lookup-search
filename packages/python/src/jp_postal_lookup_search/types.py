"""This module defines custom types."""

from typing import TypedDict

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

SpecialNotes = TypedDict(
  "SpecialNotes",
  {
    "（次のビルを除く）": list[str],
    "（その他）": list[str],
    "一円": list[str],
  },
)
