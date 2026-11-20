// This module defines custom types.

export interface SpecialNotes {
  "（次のビルを除く）": Array<string>;
  "（その他）": Array<string>;
  "一円": Array<string>;
}

export interface AddressData {
  [pref: string]: {
    [city: string]: {
      [town: string]: string
    }
  }
}

export type PrefMap = AddressData;
export type CityMap = AddressData[string];
export type TownMap = AddressData[string][string];
export type QueryMap = PrefMap | CityMap | TownMap;

export interface PostalCodeData {
  [prefCode: string]: {
    [prefData: string]: string
  }
}

export interface AddressParts {
  pref: string;
  city: string;
  town: string;

  prefKana: string;
  cityKana: string;
  townKana: string;
}
