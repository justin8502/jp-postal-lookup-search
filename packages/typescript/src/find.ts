// This module implements project-level functions.

import { CITY_TOWN_NOT_FOUND, PREFECTURE_NOT_FOUND, SEARCH_FAILED_CITY, SEARCH_FAILED_PREFECTURE, SEARCH_FAILED_TOWN } from "./constants";
import { AddressParts, CityMap, TownMap } from "./types";
import {
  addressLookupData,
  postalCodeLookupData
} from "./data";
import {
  normalizePostalCode,
  splitPostalAddress,
  searchPrefecture,
  searchCity,
  searchTown,
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
  const queryMap = addressLookupData;
  let index = 0;

  const prefectureResult = searchPrefecture(index, queryMap, address);
  const prefectureQueryMapResult = queryMap[prefectureResult.key || ""];
  index = prefectureResult.i;
  if (prefectureResult.i >= address.length || !prefectureResult.key || !prefectureQueryMapResult) return SEARCH_FAILED_PREFECTURE;
  const cityMap: CityMap = prefectureQueryMapResult;

  const cityResult = searchCity(index, cityMap, address);
  const cityQueryMapResult = cityMap[cityResult.key || ""];
  index = cityResult.i;
  if (cityResult.i >= address.length || !cityResult.key || !cityQueryMapResult) return SEARCH_FAILED_CITY;
  const townMap: TownMap = cityQueryMapResult;

  const townResult = searchTown(index, townMap, address);
  const townQueryMapResult = townMap[townResult.key || ""];
  index = townResult.i;
  if (townResult.completed && townResult.key && townQueryMapResult) return townQueryMapResult;
  return SEARCH_FAILED_TOWN;
};
