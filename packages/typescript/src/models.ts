// This module defines the PostalAddress class.

import { MATCH_7_DIGITS, STEP_LABELS } from "./constants";
import { postalCodeLookupData, addressLookupData } from "./data";
import { SpecialNotes } from "./types";
import { 
  extractQueryPositionalArguments,
  hasIchien,
  normalizePostalCode,
  normalizeStripFill,
  searchIchienOther,
  searchSpecialNotes,
  splitPostalAddress
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
    let queryMap: any = addressLookupData;
    // step: 0-prefecture 1-city 2-town
    let step = 0;
    let i = 0;
  
    let specialNotes: SpecialNotes = {
      "（次のビルを除く）": [],
      "（その他）": [],
      "一円": []
    };

    // Use a sliding window approach + lenient matches
    while (i < address.length) {
      // narrow the query by only checking keys that match the first character of target substring.
      // this significantly speeds up performance, with no loss in accuracy.
      const keysMatchingAddressFirstChar = Object.keys(queryMap).filter((key) => {
        return key[0] === address[i];
      })
      let loopCompleted = false;
      for (const key of keysMatchingAddressFirstChar) {
        const addressSubStr = address.substringUnicode(i, i + key.length);
        const [
          _normalizedQuery,
          strippedQuery,
          normalizedKey,
          strippedKey
        ] = normalizeStripFill(addressSubStr, key, specialNotes);
        // For town matches, explode number ranges and do fuzzy matching
        // e.g. 宮崎県日南市吾田東（５～１１丁目） -> 宮崎県日南市吾田東５丁目, 宮崎県日南市吾田東６丁目...
        if (step === 2) {
          if (hasIchien(strippedKey)) {
            this.processStep(step, key);
            this.initFromPostalCode(queryMap[key]);
            return;
          }
          const rangeSelectionExpandedKeys = extractQueryPositionalArguments(normalizedKey);
          // console.log(rangeSelectionExpandedKeys);
          for (const strippedExpandedKey of rangeSelectionExpandedKeys) {
            if (strippedQuery.startsWith(strippedExpandedKey) || strippedExpandedKey.startsWith(strippedQuery)) {
              this.initFromPostalCode(queryMap[key]);
              return;
            }
          }
        } else if (strippedKey.startsWith(strippedQuery)) {
          queryMap = queryMap[key];
          step += 1;
          loopCompleted = true;
          i += (key.length - 1);
          break;
        }
      }
      if (!loopCompleted) {
        const specialNote = searchSpecialNotes(address, i, specialNotes, queryMap);
        if (specialNote) {
          this.initFromPostalCode(specialNote);
          return;
        }
        i += 1;
      }
    }
  
    const ichienOther = searchIchienOther(step, queryMap);
    if (ichienOther) {
      this.initFromPostalCode(ichienOther);
      return;
    }

    console.warn(`郵便番号を検索できません。検索ステージ：${STEP_LABELS[step]}`);
  }

  private processStep(step: number, value: string): void {
    // Load Partials
    switch(step) {
      case 0:
        this.pref = value;
        break;
      case 1:
        this.city = value;
        break;
      case 2:
        this.town = value;
        break;
    }
  }
}
