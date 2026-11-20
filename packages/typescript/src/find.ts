// This module implements project-level functions.

import { CITY_TOWN_NOT_FOUND, PREFECTURE_NOT_FOUND, STEP_LABELS } from "./constants";
import { AddressData, AddressParts, CityMap, QueryMap, SpecialNotes, TownMap } from "./types";
import {
  addressLookupData,
  postalCodeLookupData
} from "./data";
import {
  extractQueryPositionalArguments,
  normalizeStripFill,
  normalizePostalCode,
  splitPostalAddress,
  searchSpecialNotes,
  hasIchien,
  searchIchienOther,
  substringUnicode,
} from "./utils";

export function lookupAddressByPostalCode(postalCode: string): string {
  const normalizedPostalCode = normalizePostalCode(postalCode);
  const [prefectureCode, cityTownCode] = splitPostalAddress(normalizedPostalCode);
  const prefectureData = postalCodeLookupData[prefectureCode];

  if (prefectureData === undefined) {
    return PREFECTURE_NOT_FOUND;
  }

  const rawPref = prefectureData["prefecture"];
  const rawCityTown = prefectureData[cityTownCode];

  if (rawPref === undefined || rawCityTown === undefined) {
    return CITY_TOWN_NOT_FOUND;
  }

  const [pref, _prefKana] = rawPref.split("|");
  const [city, town, _cityKana, _townKana] = rawCityTown.split("|");

  if (!pref || !city || !town) return "";

  return pref + city + town;
}

export function lookupAddressPartsByPostalCode(postalCode: string): AddressParts {
  const normalizedPostalCode = normalizePostalCode(postalCode);
  let addressParts: AddressParts = {
    "pref": "",
    "city": "",
    "town": "",

    "prefKana": "",
    "cityKana": "",
    "townKana": ""
  }

  const [prefectureCode, cityTownCode] = splitPostalAddress(normalizedPostalCode);
  const prefectureData = postalCodeLookupData[prefectureCode];

  if (prefectureData === undefined) {
    return addressParts;
  }

  const rawPref = prefectureData["prefecture"];
  const rawCityTown = prefectureData[cityTownCode];

  if (rawPref === undefined) {
    return addressParts
  }

  const [pref, prefKana] = rawPref.split("|");
  addressParts["pref"] = pref || "";
  addressParts["prefKana"] = prefKana || "";

  if (rawCityTown === undefined) {
    return addressParts
  }

  const [city, town, cityKana, townKana] = rawCityTown.split("|");
  addressParts["city"] = city || "";
  addressParts["town"] = town || "";
  addressParts["cityKana"] = cityKana || "";
  addressParts["townKana"] = townKana || "";

  return addressParts;
}

export function lookupAddressKanaByPostalCode(postalCode: string): string {
  const normalizedPostalCode = normalizePostalCode(postalCode);
  const [prefectureCode, cityTownCode] = splitPostalAddress(normalizedPostalCode);
  const prefectureData = postalCodeLookupData[prefectureCode];

  if (prefectureData === undefined) {
    return PREFECTURE_NOT_FOUND;
  }

  const rawPref = prefectureData["prefecture"];
  const rawCityTown = prefectureData[cityTownCode];

  if (rawPref === undefined || rawCityTown === undefined) {
    return CITY_TOWN_NOT_FOUND;
  }

  const [_pref, prefKana] = rawPref.split("|");
  const [_city, _town, cityKana, townKana] = rawCityTown.split("|");

  if (!prefKana || !cityKana || !townKana) return "";

  return prefKana + cityKana + townKana;
}

export function searchPostalCodeByAddress(address: string): string {
  let queryMap: QueryMap = addressLookupData;
  // step: 0-prefecture 1-city 2-town
  let step = 0;
  let i = 0;

  let specialNotes: SpecialNotes = {
    "（次のビルを除く）": [],
    "（その他）": [],
    "一円": []
  };

  // Use a sliding window approach + lenient matches
  while (i < address.length) {
    // narrow the query by only checking keys that match the first character of target substring.
    // this significantly speeds up performance, with no loss in accuracy.
    const keysMatchingAddressFirstChar = Object.keys(queryMap).filter((key) => {
      return key[0] === address[i];
    })
    let loopCompleted = false;
    for (const key of keysMatchingAddressFirstChar) {
      const addressSubStr = substringUnicode(address, i, i + key.length);
      const [
        _normalizedQuery,
        strippedQuery,
        normalizedKey,
        strippedKey
      ] = normalizeStripFill(addressSubStr, key, specialNotes);
      // For town matches, explode number ranges and do fuzzy matching
      // e.g. 宮崎県日南市吾田東（５～１１丁目） -> 宮崎県日南市吾田東５丁目, 宮崎県日南市吾田東６丁目...
      if (step === 2) {
        if (hasIchien(strippedKey)) {
          const townMap = queryMap as TownMap;
          return townMap[key] ?? "";
        }
        const rangeSelectionExpandedKeys = extractQueryPositionalArguments(normalizedKey);
        for (const strippedExpandedKey of rangeSelectionExpandedKeys) {
          if (strippedQuery.startsWith(strippedExpandedKey) || strippedExpandedKey.startsWith(strippedQuery)) {
            const townMap = queryMap as TownMap;
            return townMap[key] ?? "";
          }
        }
      } else if (strippedKey.startsWith(strippedQuery)) {
        if (step === 0) {
          queryMap = queryMap[key] as CityMap;
        } else if (step === 1) {
          queryMap = queryMap[key] as TownMap;
        }
        step += 1;
        loopCompleted = true;
        i += (key.length - 1);
        break;
      }
    }
    if (!loopCompleted) {
      const specialNote = searchSpecialNotes(
        address,
        i,
        specialNotes,
        step === 2 ? queryMap as TownMap : {}
      );
      if (specialNote) return specialNote;
      i += 1;
    }
  }

  if (step === 2) {
    const ichienOther = searchIchienOther(step, queryMap as TownMap);
    if (ichienOther) return ichienOther;
  }

  return `郵便番号を検索できません。検索ステージ：${STEP_LABELS[step]}`;
};
