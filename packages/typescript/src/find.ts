// This module implements project-level functions.

import {
  addressLookupData,
  postalCodeLookupData
} from "./data";
import { AddressParts } from "./types";
import {
  // extract_query_positional_arguments,
  // normalize_strip_fill,
  normalize_postal_code,
  split_postal_address,
  // search_special_notes,
  // search_ichien,
  // search_ichien_other,
} from "./utils"

export function lookupAddressByPostalCode(postalCode: string): string {
  const normalizedPostalCode = normalize_postal_code(postalCode);
  const [prefectureCode, cityTownCode] = split_postal_address(normalizedPostalCode);
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
  return {
    "pref": "",
    "city": "",
    "town": "",
    "pref_kana": "",
    "city_kana": "",
    "town_kana": ""
  }
}

export function lookupAddressKanaByPostalCode(postalCode: string): string {
  const normalizedPostalCode = normalize_postal_code(postalCode);
  const [prefectureCode, cityTownCode] = split_postal_address(normalizedPostalCode);
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