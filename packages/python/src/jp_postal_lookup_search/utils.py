"""This module provides util functions for other modules."""

import re
import unicodedata

from .types import NormalizedAddress, PrefMap, CityMap, TownMap, SearchReturn, SpecialNotes
from .constants import (
  BUILDINGS_AFTER_EXCLUDED,
  EXCLUSION_TEXT,
  NOT_LISTED_BELOW_TEXT,
  OTHER,
  SPECIAL_NOTES,
  SUFFIX_OPTIONS,
  PREFECTURE_DIGITS,
  HAS_PAREN_WITH_VALUES_COMMA,
  NUMBER_RANGE_REGEX,
  STRIP_PAREN_REGEX,
  MATCH_COMMA_REGEX,
  MATCH_DASH_REGEX,
  MATCH_POSTAL_SYMBOL_REGEX,
  MATCH_ICHI_EN
)

def extract_query_positional_arguments(address: str) -> list[str]:
  if EXCLUSION_TEXT in address: return [address]

  base = [address]
  match = re.search(HAS_PAREN_WITH_VALUES_COMMA, address)
  if match:
    no_match_prefix = address[:match.start()]
    selection = match.group(1).split("、")
    suffix_label = extract_suffix_label(selection[-1])
    base = [no_match_prefix + select + (suffix_label or "") for select in selection[:-1]] + [no_match_prefix + selection[-1]]
    res: list[str] = []
    for generated_address in base:
      match = re.search(NUMBER_RANGE_REGEX, generated_address)
      if not match:
        res.append(generated_address)
        continue

      res.extend(generate_addresses_range(generated_address, match))
    return res + [strip_paren(address)]

  match = re.search(NUMBER_RANGE_REGEX, address)
  if not match: return [strip_paren(address)]

  return generate_addresses_range(address, match) + [strip_paren(address)]

def extract_suffix_label(address: str) -> str | None:
  for suffix in SUFFIX_OPTIONS:
    if suffix in address:
      return suffix
  return None

def generate_addresses_range(address: str, match: re.Match[str]) -> list[str]:
  start, end = map(int, match.groups())

  return [ strip_paren(address[:match.start()] + str(i) + address[match.end():]) for i in range(start, end + 1) ]

def normalize_postal_code(postal_code: str) -> str:
  postal_code = unicodedata.normalize("NFKC", postal_code)
  postal_code = re.sub(MATCH_DASH_REGEX, "", postal_code)
  postal_code = re.sub(MATCH_POSTAL_SYMBOL_REGEX, "", postal_code)
  return postal_code

def normalize(address: str) -> str:
  address = unicodedata.normalize("NFKC", address)
  address = re.sub(MATCH_COMMA_REGEX, "、", address)
  address = re.sub(MATCH_DASH_REGEX, "ー", address)
  return address

def split_postal_address(address: str) -> tuple[str, str]:
  return address[0:PREFECTURE_DIGITS], address[PREFECTURE_DIGITS:]

def strip_paren(address: str) -> str:
  return re.sub(STRIP_PAREN_REGEX, "", address)

def has_ichien(key: str) -> bool:
  return bool(re.search(MATCH_ICHI_EN, key))

def search_special_notes(
  address: str,
  i: int,
  special_notes: SpecialNotes
) -> str | None:
  for note, query_list in special_notes.items():
    for final_key in query_list:
      normalized_query = normalize(address[i:i+len(final_key)-len(note)])
      if normalized_query + note == final_key:
        return final_key
  return None

def search_ichien_other(town_map: TownMap) -> str | None:
  # Explicit 一円 match
  if len(town_map) == 1:
    key = next(iter(town_map))

    if has_ichien(key):
      return key
  return NOT_LISTED_BELOW_TEXT if NOT_LISTED_BELOW_TEXT in town_map else None

def normalize_strip_fill(
  address_substr: str,
  key: str,
) -> NormalizedAddress:
  # Normalize -> Fix -/(/)/[0-9]
  # Strip -> Remove ()
  normalized_query = normalize(address_substr)
  stripped_query = strip_paren(normalized_query)
  normalized_key = normalize(key)
  stripped_key = strip_paren(normalized_key)

  return NormalizedAddress(
    normalized_query,
    stripped_query,
    normalized_key,
    stripped_key
  )

def search_prefecture(i: int, pref_map: PrefMap, address: str) -> SearchReturn:
  return _search_simple_map(i, pref_map, address)

def search_city(i: int, city_map: CityMap, address: str) -> SearchReturn:
  return _search_simple_map(i, city_map, address)

def search_town(i: int, town_map: TownMap, address: str) -> SearchReturn:
  special_notes: SpecialNotes = {
    note: queries.copy()
    for note, queries in SPECIAL_NOTES.items()
  }

  while i < len(address):
    keys_matching_address_first_char: list[str] = [key for key in town_map if key and key[0] == address[i]]
    for key in keys_matching_address_first_char:
      normalized = normalize_strip_fill(address[i:i+len(key)], key)
      stripped_query = normalized.stripped_query
      normalized_key = normalized.normalized_key
      stripped_key = normalized.stripped_key
      special_notes = _update_special_notes(key, special_notes)

      if has_ichien(stripped_key):
        i += len(key)
        return _search_result(i, key, True)
      range_selection_expanded_keys = extract_query_positional_arguments(normalized_key)
      for stripped_key in range_selection_expanded_keys:
        if stripped_query.startswith(stripped_key) or stripped_key.startswith(stripped_query):
          i += len(key)
          return _search_result(i, key, True)
    special_note = search_special_notes(address, i, special_notes)
    if special_note is not None:
      i += len(special_note)
      return _search_result(i, special_note, True)
    i += 1

  ichien_other = search_ichien_other(town_map)
  if ichien_other is not None:
    i += len(ichien_other)
    return _search_result(i, ichien_other, True)

  return _search_result(i, None, False)

def _update_special_notes(
  key: str,
  special_notes: SpecialNotes,
) -> SpecialNotes:
  updated_notes = special_notes.copy()

  for note in (BUILDINGS_AFTER_EXCLUDED, OTHER):
    if note in key and key not in special_notes[note]:
      updated_notes[note] = special_notes[note] + [key]

  return updated_notes

def _search_simple_map(
  i: int,
  query_map: PrefMap | CityMap,
  address: str,
) -> SearchReturn:
  while i < len(address):
    for key in query_map:
      if not key or key[0] != address[i]: continue
      normalized = normalize_strip_fill(address[i:i+len(key)], key)
      stripped_query = normalized.stripped_query
      stripped_key = normalized.stripped_key

      if stripped_key.startswith(stripped_query):
        i += len(key)
        return _search_result(i, key, False)

    i += 1

  return _search_result(i, None)

def _search_result(
  i: int,
  key: str | None,
  completed: bool = False
) -> SearchReturn:
  return SearchReturn(
    i = i,
    key = key,
    completed = completed
  )
