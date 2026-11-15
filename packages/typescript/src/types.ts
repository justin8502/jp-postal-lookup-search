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

export interface PostalCodeData {
  [prefCode: string]: {
    [prefData: string]: string
  }
}

export interface AddressParts {
  pref: string;
  city: string;
  town: string;

  pref_kana: string;
  city_kana: string;
  town_kana: string;
}