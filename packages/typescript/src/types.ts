// This module defines custom types.

export type PrefMap = AddressData;
export type CityMap = AddressData[string];
export type TownMap = AddressData[string][string];
export type QueryMap = PrefMap | CityMap | TownMap;

export interface AddressData {
  [pref: string]: {
    [city: string]: {
      [town: string]: string
    }
  }
}

export interface PostalCodeData {
  [prefCode: string]: {
    [prefData: string]: string
  }
}

export interface NormalizedAddress {
  normalizedQuery: string;
  strippedQuery: string;
  normalizedKey: string;
  strippedKey: string;
}

export interface AddressParts {
  pref: string;
  city: string;
  town: string;

  prefKana: string;
  cityKana: string;
  townKana: string;
}

export interface SpecialNotes {
  [key: string]: Array<string>;
}

export interface SearchReturn {
  i: number;
  key?: string;
  completed: boolean;
}
