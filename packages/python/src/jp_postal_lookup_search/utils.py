import re
import unicodedata
from .constants import (
  EXCLUSION_TEXT,
  SUFFIX_OPTIONS,
  PREFECTURE_DIGITS,
  HAS_PAREN_WITH_VALUES_COMMA,
  NUMBER_RANGE_REGEX,
  STRIP_PAREN_REGEX,
  MATCH_COMMA_REGEX,
  MATCH_DASH_REGEX
)

def extract_query_positional_arguments(addr: str) -> list[str]:
  if EXCLUSION_TEXT in addr: return [addr]

  base = [addr]
  match = re.search(HAS_PAREN_WITH_VALUES_COMMA, addr)
  if match:
    unrelated = [addr[:match.start()], addr[match.end():]]
    selection = match.group(1).split("、")
    suffix_label = extract_suffix_label(selection[-1])
    base = [unrelated[0] + select + (suffix_label or "") for select in selection[:-1]] + [unrelated[0] + selection[-1]]
    res = []
    for generated_addr in base:
      match = re.search(NUMBER_RANGE_REGEX, generated_addr)
      if not match:
        res += [generated_addr]
        continue

      res += generate_address_range(generated_addr, match) + [generated_addr]
    return res + [strip_paren(addr)]

  # match = re.search(r"(\d+)~(\d+)", addr)
  match = re.search(NUMBER_RANGE_REGEX, addr)
  if not match: return [strip_paren(addr)]

  return generate_address_range(addr, match) + [strip_paren(addr)]

def extract_suffix_label(addr: str) -> str:
  for suffix in SUFFIX_OPTIONS:
    if suffix in addr:
      return suffix

def generate_address_range(addr: str, match: re.Match[str]) -> list[str]:
  start, end = map(int, match.groups())

  return [ strip_paren(addr[:match.start()] + str(i) + addr[match.end():]) for i in range(start, end + 1) ]

def normalize(addr: str) -> str:
  addr = unicodedata.normalize("NFKC", addr)
  addr = re.sub(MATCH_COMMA_REGEX, "、", addr)
  addr = re.sub(MATCH_DASH_REGEX, "ー", addr)
  return addr

def split_postal_address(addr: str) -> tuple[str, str]:
  return addr[0:PREFECTURE_DIGITS], addr[PREFECTURE_DIGITS:]

def strip_paren(addr: str) -> str:
  return re.sub(STRIP_PAREN_REGEX, "", addr)