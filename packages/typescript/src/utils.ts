// This module provides util functions for other modules.

import {
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
} from "./constants"
import { SpecialNotes } from "./types"

export function normalizePostalCode(postalCode: string): string {
  postalCode = postalCode.normalize("NFKC")
  postalCode = postalCode.replace(MATCH_DASH_REGEX, "")
  postalCode = postalCode.replace(MATCH_POSTAL_SYMBOL_REGEX, "")
  return postalCode
}

export function normalize(address: string): string {
  address = address.normalize("NFKC");
  address = address.replace(MATCH_COMMA_REGEX, "、");
  address = address.replace(MATCH_DASH_REGEX, "ー");
  return address;
}

export function splitPostalAddress(address: string): [string, string] {
  return [address.substring(0, PREFECTURE_DIGITS), address.substring(PREFECTURE_DIGITS)]
}

export function strip_paren(address: string): string {
  return address.replace(STRIP_PAREN_REGEX, "")
}

export function hasIchien(key: string): boolean {
  return MATCH_ICHI_EN.test(key);
}

export function searchSpecialNotes(
  address: string,
  i: number,
  specialNotes: SpecialNotes,
  queryMap: any
): string {
  for (let j = 0; j < Object.keys(specialNotes).length; j++) {
    const note = Object.keys(specialNotes)[j];
    for (const finalKey of Object.values(specialNotes)[j]) {
      const targetAddrSt = i;
      const targetAddrEnd = i + (finalKey.length || 0) - (note?.length || 0);
      const addresSubStr = address.substring(targetAddrSt, targetAddrEnd)
      const normalizedQuery = normalize(addresSubStr)
      if (normalizedQuery + note === finalKey) {
        return queryMap[finalKey]
      }
    }
  }
  return ""
}

export function search_ichien_other(step: number, query_map: any): string {
  return ""
}

export function normalize_strip_fill(
  address_substr: string,
  key: string,
  special_notes: SpecialNotes
): Array<string> {
  return [""]
}
