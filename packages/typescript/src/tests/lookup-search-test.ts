// This module defines tests for find methods.

import { 
  lookupAddressByPostalCode,
  lookupAddressPartsByPostalCode,
  lookupAddressKanaByPostalCode,
  searchPostalCodeByAddress
} from "../find";

function testBulkPostalLookup() {
  const postalCodes = ["1000001", "1050022", "1500001", "1600022", "1060032", "2200011",
                  "2310011", "3300802", "2730005", "6008001", "6048006", "5300001", 
                  "5420081", "6500021", "4600008", "4500002", "8100001", "7300031", 
                  "9800021", "0600001", "9000015"];
  
  for (const postalCode of postalCodes) {
    const addressLookup = lookupAddressByPostalCode(postalCode);
    const postalLookup = searchPostalCodeByAddress(addressLookup);
    if (postalLookup !== postalCode) {
      throw new Error(
        `Mismatch for ${postalCode}: expected ${postalCode}, got ${postalLookup}`
      );
    }
  }
};

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
};

function testPostalLookupKana() {
  const postalCodesLookupKana = [{
    postalCode: "1500001",
    kana: "ﾄｳｷｮｳﾄｼﾌﾞﾔｸｼﾞﾝｸﾞｳﾏｴ"
  }, {
    postalCode: "3300802",
    kana: "ｻｲﾀﾏｹﾝｻｲﾀﾏｼｵｵﾐﾔｸﾐﾔﾁｮｳ"
  }, {
    postalCode: "2730005",
    kana: "ﾁﾊﾞｹﾝﾌﾅﾊﾞｼｼﾎﾝﾁｮｳ"
  }];
  
  postalCodesLookupKana.map((value) => {
    const addressLookupKana = lookupAddressKanaByPostalCode(value.postalCode);
    if (addressLookupKana !== value.kana) {
      throw new Error(
        `Mismatch for ${value.postalCode}: expected ${value.kana}, got ${addressLookupKana}`
      );
    }
  });
};

function testPostalLookupNormalization() {
  const postalCodes = [
    "1500001",
    "150-0001",
    "１５００００１",
    "１５０ー０００１",
    "〒１５００００１",
  ]

  const basePostalCode = "1500001"
  
  for (const postalCode of postalCodes) {
    const addressLookup = lookupAddressByPostalCode(postalCode)
    const postalLookup = searchPostalCodeByAddress(addressLookup)
    if (postalLookup !== basePostalCode) {
      throw new Error(
        `Mismatch for ${postalCode}: expected ${basePostalCode}, got ${postalLookup}`
      );
    }
  }
}

function testFuzzyMatching() {
  // テキスト正規化
  // 東京都港区赤坂（次のビルを除く）
  const tokyoTextVariance = ["東京都港区赤坂1丁目10-5", "東京都港区赤坂１丁目ー１０-５", "東京都港区赤坂1丁目10-5藤田ビル"];
  const tokyoTextVariancePostal = "1070052";

  for (const tokyoAddr of tokyoTextVariance) {
    const postalLookup = searchPostalCodeByAddress(tokyoAddr);
    if (postalLookup !== tokyoTextVariancePostal) {
      throw new Error(
        `Mismatch for ${tokyoAddr}: expected ${tokyoTextVariancePostal}, got ${postalLookup}`
      );
    }
  }

  // 丁目マッチング
  // 宮崎県日南市吾田東（５～１１丁目）
  const miyazakiChome = ["宮崎県日南市吾田東５丁目", "宮崎県日南市吾田東６丁目", "宮崎県日南市吾田東７丁目ー１ー２"];
  const miyazakiPostal = "8892541";

  for (const miyazakiAddr of miyazakiChome) {
    const postalLookup = searchPostalCodeByAddress(miyazakiAddr);
    if (postalLookup !== miyazakiPostal) {
      throw new Error(
        `Mismatch for ${miyazakiAddr}: expected ${miyazakiPostal}, got ${postalLookup}`
      );
    }
  }

  // 北海道札幌市中央区北一条西（１～１９丁目）
  const hokkaidoFuzzy = ["北海道札幌市中央区北一条西９丁目", "北海道札幌市中央区北一条西１4丁目", "北海道札幌市中央区北一条西１９丁目"];
  const hokkaidoFuzzyPostal = "0600001";
  
  for (const hokkaidoAddr of hokkaidoFuzzy) {
    const postalLookup = searchPostalCodeByAddress(hokkaidoAddr);
    if (postalLookup !== hokkaidoFuzzyPostal) {
      throw new Error(
        `Mismatch for ${hokkaidoAddr}: expected ${hokkaidoFuzzyPostal}, got ${postalLookup}`
      );
    }
  }
}

function testSpecialCases() {
  // 一円
  // 長野県北安曇郡松川村松川村一円
  const ichienPostal = "3998501";
  const ichienAddress = "長野県北安曇郡松川村松川村一円";
  const postalLookup = searchPostalCodeByAddress(ichienAddress);
  if (postalLookup !== ichienPostal) {
    throw new Error(
      `Mismatch for ${ichienAddress}: expected ${ichienPostal}, got ${postalLookup}`
    );
  }
  const ichienAddressShort = "長野県北安曇郡松川村松川村";
  const postalLookupShort = searchPostalCodeByAddress(ichienAddressShort);
  if (postalLookup !== postalLookupShort) {
    throw new Error(
      `Mismatch for ${ichienAddressShort}: expected ${postalLookup}, got ${postalLookupShort}`
    );
  }

  // その他
  const tokyoShinjukuPostal = "1620052";
  const tokyoShinjukuOther = "東京都新宿区戸山公園";
  const tokyoShinjukuPostalLookup = searchPostalCodeByAddress(tokyoShinjukuOther);
  if (tokyoShinjukuPostalLookup !== tokyoShinjukuPostal) {
    throw new Error(
      `Mismatch for ${tokyoShinjukuOther}: expected ${tokyoShinjukuPostal}, got ${tokyoShinjukuPostalLookup}`
    );
  }

  // 以下に掲載がない場合
  const fukuokaKogePostal = "8710900";
  const fukuokaKogeOther = "福岡県築上郡上毛町近所医者";
  const fukuokaKogePostalLookup = searchPostalCodeByAddress(fukuokaKogeOther);
  if (fukuokaKogePostalLookup !== fukuokaKogePostal) {
    throw new Error(
      `Mismatch for ${fukuokaKogeOther}: expected ${fukuokaKogePostal}, got ${fukuokaKogePostalLookup}`
    );
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
};

function testInvalidInput() {
  const invalidPostal1 = "0000000";
  const invalidPostal2 = "0101010";
  const invalidAddress1 = "東京都沖縄";
  const invalidAddress2 = "50 Hudson Yards, New York, NY 10001, United States";

  const invalidLookupPrefText = "都道府県情報を検索できません。";
  const invalidLookupText = "住所情報を検索できません。";
  const invalidSearchText1 = "郵便番号を検索できません。検索ステージ：市区町村";
  const invalidSearchText2 = "郵便番号を検索できません。検索ステージ：都道府県";

  const postalLookup1 = lookupAddressByPostalCode(invalidPostal1);
  if (postalLookup1 !== invalidLookupPrefText) {
    throw new Error(
      `Mismatch for ${invalidPostal1}: expected ${invalidLookupPrefText}, got ${postalLookup1}`
    );
  }

  const postalLookup2 = lookupAddressByPostalCode(invalidPostal2)
  if (postalLookup2 !== invalidLookupText) {
    throw new Error(
      `Mismatch for ${invalidPostal2}: expected ${invalidLookupText}, got ${postalLookup2}`
    );
  }

  const addressLookup1 = searchPostalCodeByAddress(invalidAddress1)
  if (addressLookup1 !== invalidSearchText1) {
    throw new Error(
      `Mismatch for ${invalidAddress1}: expected ${invalidSearchText1}, got ${addressLookup1}`
    );
  }

  const addressLookup2 = searchPostalCodeByAddress(invalidAddress2)
  if (addressLookup2 !== invalidSearchText2) {
    throw new Error(
      `Mismatch for ${invalidAddress2}: expected ${invalidSearchText2}, got ${addressLookup2}`
    );
  }
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
};

testBulkPostalLookup();
testPostalLookupParts();
testPostalLookupKana();
testPostalLookupNormalization();
testFuzzyMatching();
testSpecialCases();
testInvalidInput();
benchmarkLookupFind();
