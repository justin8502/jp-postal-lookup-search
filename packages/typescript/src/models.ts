// This module defines the PostalAddress class.

import { MATCH_7_DIGITS, SEARCH_FAILED_CITY, SEARCH_FAILED_PREFECTURE, SEARCH_FAILED_TOWN } from "./constants";
import { postalCodeLookupData, addressLookupData } from "./data";
import { CityMap, TownMap } from "./types";
import { 
  normalizePostalCode,
  searchCity,
  searchPrefecture,
  searchTown,
  splitPostalAddress,
} from "./utils";

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

  equals(address: PostalAddress): boolean {
    return this.getPostalCode() === address.getPostalCode();
  }

  strictEquals(address: PostalAddress): boolean {
    return (this.getPostalCode() === address.getPostalCode()) &&
      (this.pref === address.pref) &&
      (this.city === address.city) &&
      (this.town === address.town) &&
      (this.prefKana === address.prefKana) &&
      (this.cityKana === address.cityKana) &&
      (this.townKana === address.townKana);
  }

  getPostalCode(): string {
    return this.postalCode;
  }

  getKana(): string {
    return (this.custom["prefKana"] || this.prefKana) + 
      (this.custom["cityKana"] || this.cityKana) +
      (this.custom["townKana"] || this.townKana) +
      (this.custom["streetKana"] || this.streetKana) +
      (this.custom["buildingKana"] || this.buildingKana);
  }

  getAddress(): string {
    return (this.custom["pref"] || this.pref) + 
      (this.custom["city"] || this.city) +
      (this.custom["town"] || this.town) +
      (this.custom["street"] || this.street) +
      (this.custom["building"] || this.building);
  }

  update(values: PostalAddressCustom): void {
    if (values.pref) this.pref = values.pref;
    if (values.city) this.city = values.city;
    if (values.town) this.town = values.town;
    if (values.street) this.street = values.street;
    if (values.building) this.building = values.building;

    if (values.prefKana) this.prefKana = values.prefKana;
    if (values.cityKana) this.cityKana = values.cityKana;
    if (values.townKana) this.townKana = values.townKana;
    if (values.streetKana) this.streetKana = values.streetKana;
    if (values.buildingKana) this.buildingKana = values.buildingKana;
  }

  updateCustom(custom: PostalAddressCustom): void {
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
      this.initFromPostalCode(normalizedAddress);
    } else {
      this.initFromAddress(this.pref + this.city + this.town);
    }
    if (!keepCustom) {
      this.updateCustom({}); 
    }
  }

  private initFromValue(value: string): void {
    const normalizedAddress = normalizePostalCode(value);
    if (MATCH_7_DIGITS.test(normalizedAddress)) {
      this.initFromPostalCode(normalizedAddress);
    }
    else {
      this.initFromAddress(value);
    }
  }

  private initFromPostalCode(postalCode: string) {
    this.setDefaultValues();
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
  
  private initFromAddress(address: string) {
    const queryMap = addressLookupData;
    let index = 0;
  
    const prefectureResult = searchPrefecture(index, queryMap, address);
    const prefectureQueryMapResult = queryMap[prefectureResult.key || ""];
    index = prefectureResult.i;
    if (prefectureResult.i >= address.length || !prefectureResult.key || !prefectureQueryMapResult) {
      console.warn(SEARCH_FAILED_PREFECTURE)
      return;
    }
    const cityMap: CityMap = prefectureQueryMapResult;
  
    const cityResult = searchCity(index, cityMap, address);
    const cityQueryMapResult = cityMap[cityResult.key || ""];
    index = cityResult.i;
    if (cityResult.i >= address.length || !cityResult.key || !cityQueryMapResult) {
      console.warn(SEARCH_FAILED_CITY)
      return;
    }
    const townMap: TownMap = cityQueryMapResult;
  
    const townResult = searchTown(index, townMap, address);
    const townQueryMapResult = townMap[townResult.key || ""];
    index = townResult.i;
    if (townResult.completed && townResult.key && townQueryMapResult) {
      this.initFromPostalCode(townQueryMapResult)
      return;
    }
    console.warn(SEARCH_FAILED_TOWN)
  }

  private setDefaultValues() {
    this.setPostal("");

    this.pref = "";
    this.city = "";
    this.town = "";
    this.street = "";
    this.building = "";

    this.prefKana = "";
    this.cityKana = "";
    this.townKana = "";
    this.streetKana = "";
    this.buildingKana = "";
  }
}
