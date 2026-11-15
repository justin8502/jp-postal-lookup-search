// This module implements project-level functions.

import {
  addressLookupData,
  postalCodeLookupData
} from "./data";
import { AddressParts } from "./types";
import {
  // extract_query_positional_arguments,
  // normalize_strip_fill,
  normalizePostalCode,
  splitPostalAddress,
  searchSpecialNotes,
  hasIchien,
  // search_ichien_other,
} from "./utils"

export function lookupAddressByPostalCode(postalCode: string): string {
  const normalizedPostalCode = normalizePostalCode(postalCode);
  const [prefectureCode, cityTownCode] = splitPostalAddress(normalizedPostalCode);
  const prefectureData = postalCodeLookupData[prefectureCode];

  if (prefectureData === undefined) {
    return "都道府県情報を検索できません。";
  }

  const rawPref = prefectureData["prefecture"];
  const rawCityTown = prefectureData[cityTownCode];

  if (rawPref === undefined || rawCityTown === undefined) {
    return "住所情報を検索できません。";
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

  return addressParts
}

export function lookupAddressKanaByPostalCode(postalCode: string): string {
  const normalizedPostalCode = normalizePostalCode(postalCode);
  const [prefectureCode, cityTownCode] = splitPostalAddress(normalizedPostalCode);
  const prefectureData = postalCodeLookupData[prefectureCode];

  if (prefectureData === undefined) {
    return "都道府県情報を検索できません。";
  }

  const rawPref = prefectureData["prefecture"];
  const rawCityTown = prefectureData[cityTownCode];

  if (rawPref === undefined || rawCityTown === undefined) {
    return "住所情報を検索できません。";
  }

  const [_pref, prefKana] = rawPref.split("|");
  const [_city, _town, cityKana, townKana] = rawCityTown.split("|");

  if (!prefKana || !cityKana || !townKana) return "";

  return prefKana + cityKana + townKana;
}

export function searchPostalCodeByAddress(address: string): string {
  return ""
}
