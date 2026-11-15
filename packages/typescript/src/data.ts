// This module handles loading the prebuilt json files.

import addressLookupJson from "./data/address_lookup.json";
import postalCodeLookupJson from "./data/postal_code_lookup.json";
import { AddressData, PostalCodeData } from "./types";

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isAddressLookupData(raw: unknown): raw is AddressData {
  if (!isRecord(raw)) return false;

  return Object.values(raw).every((cities) => {
    if (!isRecord(cities)) return false;

    return Object.values(cities).every((towns) => {
      if (!isRecord(towns)) return false;

      return Object.values(towns).every(
        (town) => typeof town === "string"
      );
    });
  });
}

function isPostalCodeLookupData(raw: unknown): raw is PostalCodeData {
  if (!isRecord(raw)) return false;

  return Object.values(raw).every((prefData) => {
    if (!isRecord(prefData)) return false;

    return Object.values(prefData).every(
      (value) => typeof value === "string"
    );
  });
}

if (!isPostalCodeLookupData(postalCodeLookupJson) || !isAddressLookupData(addressLookupJson)) {
  throw new Error("Invalid JSON structure");
}

export const addressLookupData: AddressData = addressLookupJson;
export const postalCodeLookupData: PostalCodeData = postalCodeLookupJson;