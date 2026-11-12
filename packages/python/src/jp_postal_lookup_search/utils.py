"""This module provides util functions for other modules."""

import re
from typing import Dict
import unicodedata
from .constants import (
  EXCLUSION_TEXT,
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
    no_match_groups = [address[:match.start()], address[match.end():]]
    selection = match.group(1).split("、")
    suffix_label = extract_suffix_label(selection[-1])
    base = [no_match_groups[0] + select + (suffix_label or "") for select in selection[:-1]] + [no_match_groups[0] + selection[-1]]
    res = []
    for generated_address in base:
      match = re.search(NUMBER_RANGE_REGEX, generated_address)
      if not match:
        res += [generated_address]
        continue

      res += generate_addressess_range(generated_address, match) + [generated_address]
    return res + [strip_paren(address)]

  match = re.search(NUMBER_RANGE_REGEX, address)
  if not match: return [strip_paren(address)]

  return generate_addressess_range(address, match) + [strip_paren(address)]

def extract_suffix_label(address: str) -> str:
  for suffix in SUFFIX_OPTIONS:
    if suffix in address:
      return suffix

def generate_addressess_range(address: str, match: re.Match[str]) -> list[str]:
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

def search_ichien(key) -> str:
  re.search(MATCH_ICHI_EN, key)

def search_special_notes(
  address: str,
  i: int,
  special_notes: Dict[str, list[str]],
  query_map: Dict
) -> str:
  for note, query_list in special_notes.items():
    for final_key in query_list:
      normalized_query = normalize(address[i:i+len(final_key)-len(note)])
      if normalized_query + note == final_key:
        return query_map[final_key]
  return ""

def search_ichien_other(step: int, query_map: Dict) -> str:
  if step == 2:
    # Explicit 一円 match
    if len(query_map) == 1:
      key: str = next(iter(query_map))

      if search_ichien(key):
        return query_map[key]
    return query_map.get("以下に掲載がない場合", "")
  return ""

def normalize_strip_fill(
  address_substr: str,
  key: str,
  special_notes: Dict[str, list[str]]
) -> list[str]:
  # Normalize -> Fix -/(/)/[0-9]
  # Strip -> Remove ()
  normalized_query = normalize(address_substr)
  stripped_query = strip_paren(normalized_query)
  normalized_key = normalize(key)
  stripped_key = strip_paren(normalized_key)
  if "（次のビルを除く）" in key:
    special_notes["（次のビルを除く）"] += [key]
  if "（その他）" in key:
    special_notes["（その他）"] += [key]

  return [normalized_query, stripped_query, normalized_key, stripped_key]