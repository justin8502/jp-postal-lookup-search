// This module defines the PostalAddress class.

import { MATCH_7_DIGITS } from "./constants";
import { postalCodeLookupData } from "./data";
import { normalizePostalCode, splitPostalAddress } from "./utils";

interface PostalAddressCustom {
  pref?: string;
  city?: string;
  town?: string;
  street?: string;
  building?: string;

  prefKana?: string;
  cityKana?: string;
  townKana?: string;
  streetKana?: string;
  buildingKana?: string;
}

export class PostalAddress {
  pref = "";
  city = "";
  town = "";
  street = "";
  building = "";

  prefKana = "";
  cityKana = "";
  townKana = "";
  streetKana = "";
  buildingKana = "";

  protected postalCode = "";

  protected custom: PostalAddressCustom = {};

  constructor(value: string, custom?: PostalAddressCustom) {
    if (value) {
      this.initFromValue(value);
    }

    // Custom acts as a mask, but does not change the underlying properties.
    // This allows us to manipulate custom independently from the data
    // loaded from address/postal/code
    this.custom = custom ?? {};
  }

  getPostalCode(): string {
    return this.postalCode;
  }

  getKana(): string {
    return (this.custom["prefKana"] || this.prefKana) + 
      (this.custom["cityKana"] || this.cityKana) +
      (this.custom["townKana"] || this.townKana) +
      (this.custom["streetKana"] || this.streetKana) +
      (this.custom["buildingKana"] || this.buildingKana)
  }

  getAddress(): string {
    return (this.custom["pref"] || this.pref) + 
      (this.custom["city"] || this.city) +
      (this.custom["town"] || this.town) +
      (this.custom["street"] || this.street) +
      (this.custom["building"] || this.building)
  }

  update(custom: PostalAddressCustom): void {
    const postalAddressCustomKeys: (keyof PostalAddressCustom)[] = [
      "pref", "city", "town", "street", "building",
      "prefKana", "cityKana", "townKana", "streetKana", "buildingKana"
    ];
    let newCustom: PostalAddressCustom = {};
    for (const key of postalAddressCustomKeys) {
      if (key in custom) {
        newCustom[key] = custom[key];
      }
    }

    this.custom = newCustom;
  }

  setPostal(postalCode: string): void {
    this.postalCode = postalCode;
  }

  reload(keepCustom: boolean = true) {
    const normalizedAddress = normalizePostalCode(this.getPostalCode())
    if (MATCH_7_DIGITS.test(normalizedAddress)) {
      this.initFromPostalCode(normalizedAddress)
    }
      // self._init_from_address(self.pref + self.city + self.town)
    if (!keepCustom) {
      this.update({}); 
    }
  }

  private initFromValue(value: string): void {
    const normalizedAddress = normalizePostalCode(value)
    if (MATCH_7_DIGITS.test(normalizedAddress)) {
      this.initFromPostalCode(normalizedAddress)
    }
    // else:
    //   self._init_from_address(value)
  }

  private initFromPostalCode(postalCode: string) {
    this.setPostal(postalCode);
    
    const [prefectureCode, cityTownCode] = splitPostalAddress(postalCode);
    const prefectureData = postalCodeLookupData[prefectureCode];
  
    if (prefectureData === undefined) {
      console.log(`郵便番号の該当都道府県を検索できません： ${postalCode}`);
      return;
    }
  
    const rawPref = prefectureData["prefecture"];
    const rawCityTown = prefectureData[cityTownCode];
  
    if (rawPref === undefined) {
      console.log(`郵便番号の該当都道府県を検索できません： ${postalCode}`);
      return;
    }
  
    const [pref, prefKana] = rawPref.split("|");
    this.pref = pref || "";
    this.prefKana = prefKana || "";
  
    if (rawCityTown === undefined) {
      console.log(`郵便番号の該当住所を検索できません： ${postalCode}`);
      return;
    }
  
    const [city, town, cityKana, townKana] = rawCityTown.split("|");
    this.city = city || "";
    this.town = town || "";
    this.cityKana = cityKana || "";
    this.townKana = townKana || "";
  }
}
