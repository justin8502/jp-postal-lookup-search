# JP Postal Lookup Search
[![npm version](https://img.shields.io/npm/v/jp-postal-lookup-search?style=flat-square&logo=npm)](https://www.npmjs.com/package/jp-postal-lookup-search)
![CI/CD](https://github.com/justin8502/jp-postal-lookup-search/actions/workflows/ci-typescript.yml/badge.svg)

※日本語版が続きます

A synchronous, dependency-free Japanese postal code and address lookup library.
Supports postal code-to-address lookups, address-to-postal code searches, partial matching, and customizable address overrides.
Functionality and dataset is built around the official Japan Post ken_all dataset. 

Supports partial/incomplete matching, local overrides (see usage). 

[Try the interactive demo on CodePen](https://codepen.io/justin8502/pen/GgmZwEo)

Example:
```ts
import {
  lookupAddressByPostalCode,
  searchPostalCodeByAddress,
} from 'jp-postal-lookup-search';

...

const addr = lookupAddressByPostalCode("6500021")
const postalCode = searchPostalCodeByAddress("兵庫県神戸市中央区三宮町")
```

---

このプロジェクトでは、郵便番号から住所を検索したり、住所から郵便番号を検索したりできます。
コールバック関数厳禁🙅‍♂️・依存パッケージなし😎・使いやすい👍パッケージです。
日本郵便の公式サイトで公開されている郵便番号データ（KEN_ALL）を使用しています。

部分一致・不完全な住所での検索や、ローカルでの上書き設定にも対応しています（Usageを参照）。

[DEMOを試してみる](https://codepen.io/justin8502/pen/GgmZwEo)

例：
```ts
import {
  lookupAddressByPostalCode,
  searchPostalCodeByAddress,
} from 'jp-postal-lookup-search';

...

const addr = lookupAddressByPostalCode("6500021")
const postalCode = searchPostalCodeByAddress("兵庫県神戸市中央区三宮町")
```

## Methods

| Method / 関数 | Description / 説明 | Example / 例 | Speed / 速度 |
|---|---|---|---|
| `lookupAddressByPostalCode(postalCode)` | Looks up address associated with postal code / 郵便番号から住所を検索します。 | `lookupAddressByPostalCode("6500021")` | ~2.169 µs / call |
| `lookupAddressPartsByPostalCode(postalCode)` | Looks up address associated with postal code and returns object with properties / 郵便番号から住所を検索します。 | `lookupAddressPartsByPostalCode("6500021")` | ~1.977 µs / call |
| `lookupAddressKanaByPostalCode(postalCode)` | Looks up address (in kana) associated with postal code / 郵便番号から住所のカナ表記を検索します。 | `lookupAddressKanaByPostalCode("6500021")` | ~1.971 µs / call |
| `searchPostalCodeByAddress(address)` | Matches address to a postal code / 住所から郵便番号を検索します。 | `searchPostalCodeByAddress("兵庫県神戸市中央区三宮町")` | ~132.369 µs / call |

## Usage

Installation
```
npm install jp-postal-lookup-search
```
Importing methods & PostalAddress class
```ts
import {
  lookupAddressByPostalCode,
  lookupAddressPartsByPostalCode,
  lookupAddressKanaByPostalCode,
  searchPostalCodeByAddress,
  PostalAddress
} from 'jp-postal-lookup-search';
```

This project is ideal for React lifecycle methods, such as useState/useEffect.

```ts
const [pref, setPref] = useState("");
const [city, setCity] = useState("");
const [town, setTown] = useState("");
...

useEffect(() => {
  if (postalCode.length !== 7) return;
  
  const {
    pref,
    city,
    town
  } = lookupAddressPartsByPostalCode(postalCode);
  setPref(pref);
  setCity(city);
  setTown(town);
}, [postalCode]);
```

Here is another example syncing a postalCode state variable to a passed address prop (or an error code, if it does not exist).
```ts
const { address } = props;
const [postalCode, setPostalCode] = useState(
  searchPostalCodeByAddress(address)
);
...

useEffect(() => {
  setPostalCode(searchPostalCodeByAddress(address));
}, [address]);
```

In addition to the packaged methods, this package also exposes a PostalAddress class 
that can be used to manage prefecture/city/town information. 

```ts
const sampleLocation = new PostalAddress("6008001");
// 京都府京都市下京区真町
sampleLocation.update(
  {
    "pref": "東京都",
    "prefKana": "ﾄｳｷｮｳﾄ",
  }
);
console.log(sampleLocation.getAddress());
// 東京都京都市下京区真町

const sampleLocation2 = new PostalAddress("6008001");
const sampleLocation3 = new PostalAddress("埼玉県さいたま市大宮区宮町");
// custom
const sampleLocation4 = new PostalAddress("1020075",
  {
    "street": "6-16",
    "building": "二松学舎大学 九段1・2号館",
    "streetKana": "6-16ﾆｼｮｳｶﾞｸｼｬﾀﾞｲｶﾞｸ",
    "buildingKana": "ｸﾀﾞﾝ1･2ｺﾞｳｶﾝ"
  }
);

const locationEnKana = new PostalAddress("1110032", 
  {
    "prefKana": "Tokyo-To ",
    "cityKana": "Taito-Ku ",
    "townKana": "Asakusa ",
    "streetKana": "2 Chome-3-1"
  }
);
console.log(locationEnKana.getKana());
// Tokyo-To Taito-Ku Asakusa 2 Chome-3-1
```

---

インストール
```
npm install jp-postal-lookup-search
```
関数およびPostalAddressのインポート
```ts
import {
  lookupAddressByPostalCode,
  lookupAddressPartsByPostalCode,
  lookupAddressKanaByPostalCode,
  searchPostalCodeByAddress,
  PostalAddress
} from 'jp-postal-lookup-search';
```

こちらのメソッドは、useStateやuseEffectなどのReactライフサイクルフックとの併用に適しています。

```ts
const [pref, setPref] = useState("");
const [city, setCity] = useState("");
const [town, setTown] = useState("");
...

useEffect(() => {
  if (postalCode.length !== 7) return;
  
  const {
    pref,
    city,
    town
  } = lookupAddressPartsByPostalCode(postalCode);
  setPref(pref);
  setCity(city);
  setTown(town);
}, [postalCode]);
```

渡された住所に対応する郵便番号をpostalCodeに反映する例です。該当する郵便番号が存在しない場合は、エラーコードが返されます。

```ts
const { address } = props;
const [postalCode, setPostalCode] = useState(
  searchPostalCodeByAddress(address)
);
...

useEffect(() => {
  setPostalCode(searchPostalCodeByAddress(address));
}, [address]);
```

メソッドに加えて、PostalAddressで都道府県・市区町村・町域など情報を取得・調整できます。

```ts
const sampleLocation = new PostalAddress("6008001");
// 京都府京都市下京区真町
sampleLocation.update(
  {
    "pref": "東京都",
    "prefKana": "ﾄｳｷｮｳﾄ",
  }
);
console.log(sampleLocation.getAddress());
// 東京都京都市下京区真町

const sampleLocation2 = new PostalAddress("6008001");
const sampleLocation3 = new PostalAddress("埼玉県さいたま市大宮区宮町");
// custom
const sampleLocation4 = new PostalAddress("1020075",
  {
    "street": "6-16",
    "building": "二松学舎大学 九段1・2号館",
    "streetKana": "6-16ﾆｼｮｳｶﾞｸｼｬﾀﾞｲｶﾞｸ",
    "buildingKana": "ｸﾀﾞﾝ1･2ｺﾞｳｶﾝ"
  }
);

const locationEnKana = new PostalAddress("1110032", 
  {
    "prefKana": "Tokyo-To ",
    "cityKana": "Taito-Ku ",
    "townKana": "Asakusa ",
    "streetKana": "2 Chome-3-1"
  }
);
console.log(locationEnKana.getKana());
// Tokyo-To Taito-Ku Asakusa 2 Chome-3-1
```

## Development

The development of this project is guided by 4 principles:
1. No callbacks. Everything should be synchronous
2. Reduce/Eliminate external dependencies
3. Emphasize usability, performance, extensibility
4. Keep static files small in size

---

このプロジェクトの実装中心点は以下になります：
1. コールバック関数厳禁
2. 依存パッケージなし
3. 使いやすさ・拡張性・処理速度を重視
4. 必要ファイル量減少

## Future Goals

EN Translations, Github Actions Automatic Update/Build