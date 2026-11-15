// This module defines the PostalAddress class.

interface PostalAddressCustom {
  pref: string;
  city: string;
  town: string;
  street: string;
  building: string;

  pref_kana: string;
  city_kana: string;
  town_kana: string;
  street_kana: string;
  building_kana: string;
}

export class PostalAddress {
  pref = "";
  city = "";
  town = "";
  street = "";
  building = "";

  pref_kana = "";
  city_kana = "";
  town_kana = "";
  street_kana = "";
  building_kana = "";

  constructor(value: string, custom?: PostalAddressCustom) {
  }
}