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
} from "./constants";
import { SpecialNotes } from "./types";

export function extractQueryPositionalArguments(address: string): Array<string> {
  if (address.includes(EXCLUSION_TEXT)) return [address];

  let base = [address];
  const match = address.match(HAS_PAREN_WITH_VALUES_COMMA);
  if (match) {
    const noMatchGroups = [
      address.slice(0, match.index),
      address.slice((match.index || 0) + match[0].length)
    ];
    const selection = noMatchGroups[1]?.split("、") || [""];
    const suffixLabel = extractSuffixLabel(selection[selection.length - 1] ?? "");
  }
  return base;
};

export function extractSuffixLabel(address: string): string {
  for (const suffix of SUFFIX_OPTIONS) {
    if (address.includes(suffix)) {
      return suffix;
    }
  }
  return "";
}

export function normalizePostalCode(postalCode: string): string {
  postalCode = postalCode.normalize("NFKC");
  postalCode = postalCode.replace(MATCH_DASH_REGEX, "");
  postalCode = postalCode.replace(MATCH_POSTAL_SYMBOL_REGEX, "");
  return postalCode;
};

export function normalize(address: string): string {
  address = address.normalize("NFKC");
  address = address.replace(MATCH_COMMA_REGEX, "、");
  address = address.replace(MATCH_DASH_REGEX, "ー");
  return address;
};

export function splitPostalAddress(address: string): [string, string] {
  return [address.substring(0, PREFECTURE_DIGITS), address.substring(PREFECTURE_DIGITS)];
};

export function stripParen(address: string): string {
  return address.replace(STRIP_PAREN_REGEX, "");
};

export function hasIchien(key: string): boolean {
  return MATCH_ICHI_EN.test(key);
};

export function searchSpecialNotes(
  address: string,
  i: number,
  specialNotes: SpecialNotes,
  queryMap: {[key: string]: string}
): string {
  // Explicit Typing
  const specialNoteEntries = Object.entries(specialNotes) as [keyof SpecialNotes, string[]][];
  for (const [note, finalKeys] of specialNoteEntries) {
    for (const finalKey of finalKeys) {
      const targetAddrSt = i;
      const targetAddrEnd = i + (finalKey.length || 0) - (note?.length || 0);
      const addresSubStr = address.substring(targetAddrSt, targetAddrEnd);
      const normalizedQuery = normalize(addresSubStr);
      if (normalizedQuery + note === finalKey) {
        return queryMap[finalKey] || "";
      }
    }
  }
  return "";
};

export function searchIchienOther(step: number, queryMap: {[key: string]: string}): string {
  if (step == 2) {
    if (Object.keys(queryMap).length == 1) {
      const queryMapKey = Object.keys(queryMap)[0] || "";
      const queryMapValue = Object.values(queryMap)[0] || "";
      if (hasIchien(queryMapKey)) {
        return queryMapValue;
      }
    }
    return queryMap["以下に掲載がない場合"] || "";
  }
  return "";
};

export function normalizeStripFill(
  addressSubStr: string,
  key: string,
  specialNotes: SpecialNotes
): [string, string, string, string] {
  // Normalize -> Fix -/(/)/[0-9]
  // Strip -> Remove ()
  const normalizedQuery = normalize(addressSubStr);
  const strippedQuery = stripParen(normalizedQuery);
  const normalizedKey = normalize(key);
  const strippedKey = stripParen(normalizedKey);
  if (key.includes("（次のビルを除く）")) {
    specialNotes["（次のビルを除く）"].push(key);
  }
  if (key.includes("（その他）")) {
    specialNotes["（その他）"].push(key);
  }

  return [normalizedQuery, strippedQuery, normalizedKey, strippedKey];
};
