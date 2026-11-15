// This module defines tests for find methods.

import { 
  lookupAddressByPostalCode,
  lookupAddressPartsByPostalCode,
  lookupAddressKanaByPostalCode,
  searchPostalCodeByAddress
} from "../find";

function testPostalLookupParts() {
  const postalCodes = ["1500001", "3300802", "4500002"]

  for (const postalCode of postalCodes) {
    const addressLookup = lookupAddressByPostalCode(postalCode)
    const addressLookupParts = lookupAddressPartsByPostalCode(postalCode)

    const addressLookupPartsCombined = [
      addressLookupParts["pref"],
      addressLookupParts["city"],
      addressLookupParts["town"]
    ].join("")
    if (addressLookup !== addressLookupPartsCombined) {
      throw new Error(
        `Mismatch for ${postalCode}: expected ${addressLookup}, got ${addressLookupPartsCombined}`
      );
    }
  }
}

function benchmarkLookupFind() {
  const postalCodes = ["1000001", "1050022", "1500001", "1600022", "1060032", "2200011", 
                       "2310011", "3300802", "2730005", "6008001"];

  const addresses = ["東京都千代田区千代田", "東京都港区海岸（１、２丁目）", "東京都渋谷区神宮前",
                     "東京都新宿区新宿", "東京都港区六本木（次のビルを除く）", "神奈川県横浜市西区高島",
                     "神奈川県横浜市中区太田町", "埼玉県さいたま市大宮区宮町", "千葉県船橋市本町",
                     "京都府京都市下京区真町"];

  // perform 10000 postal code/part/kana lookups
  printBenchMarkTest(lookupAddressByPostalCode, postalCodes)
  printBenchMarkTest(lookupAddressPartsByPostalCode, postalCodes)
  printBenchMarkTest(lookupAddressKanaByPostalCode, postalCodes)

  // perform 10000 searches
  printBenchMarkTest(searchPostalCodeByAddress, addresses)

  // perform 10000 lookups/searches
  const lookupAddressByPostalCodeSearch = (postalCode: string) => {
    const lookupAddress = lookupAddressByPostalCode(postalCode);
    searchPostalCodeByAddress(lookupAddress)
  }
  printBenchMarkTest(lookupAddressByPostalCodeSearch, postalCodes)
}

function printBenchMarkTest(func: Function, input: Array<string>) {
  const tBenchMarkSt = Date.now();
  for (let i = 0; i < 1000; i++) {
    for (const postalCode of input) {
      func(postalCode);
    }
  }
  const tBenchMarkEnd = Date.now();
  const elapsedMsPerCall = (tBenchMarkEnd - tBenchMarkSt) / (1000 * input.length);
  console.log(`${func.name}: ${elapsedMsPerCall.toFixed(6)} ms/call`);
}

testPostalLookupParts();
benchmarkLookupFind();
