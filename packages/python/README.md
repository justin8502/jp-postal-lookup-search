# JP Postal Lookup Search
※日本語版が続きます

A project that allows lookups/searches based on japanese addresses and postal codes. 
Functionality and dataset is built around the official Japan Post ken_all dataset. 

Supports partial/incomplete matching, local overrides (see usage). 

Example:
```
lookup_address_by_postal_code("6500021") -> "兵庫県神戸市中央区三宮町"
search_postal_code_by_address("兵庫県神戸市中央区三宮町") -> "6500021"

lookup_address_by_postal_code("0600001") -> "北海道札幌市中央区北一条西（１～１９丁目）"
search_postal_code_by_address("北海道札幌市中央区北一条西９丁目") -> "0600001"
```

---

このプロジェクトでは、郵便番号から住所を検索したり、住所から郵便番号を検索したりできます。
日本郵便の公式サイトで公開されている郵便番号データ（KEN_ALL）を使用しています。

部分一致・不完全な住所での検索や、ローカルでの上書き設定にも対応しています（Usageを参照）。

例：
```
lookup_address_by_postal_code("6500021") -> "兵庫県神戸市中央区三宮町"
search_postal_code_by_address("兵庫県神戸市中央区三宮町") -> "6500021"

lookup_address_by_postal_code("0600001") -> "北海道札幌市中央区北一条西（１～１９丁目）"
search_postal_code_by_address("北海道札幌市中央区北一条西９丁目") -> "0600001"
```

## Methods

| Method / 関数 | Description / 説明 | Example / 例 | Speed / 速度 |
|---|---|---|---|
| `lookup_address_by_postal_code(postal_code)` | Looks up address associated with postal code / 郵便番号から住所を検索します。 | `lookup_address_by_postal_code("6500021")` | ~0.724 µs / call |
| `lookup_address_by_postal_code_kana(postal_code)` | Looks up address (in kana) associated with postal code / 郵便番号から住所のカナ表記を検索します。 | `lookup_address_by_postal_code_kana("6500021")` | ~0.835 µs / call |
| `search_postal_code_by_address(address)` | Matches address to a postal code / 住所から郵便番号を検索します。 | `search_postal_code_by_address("兵庫県神戸市中央区三宮町")` | ~313.507 µs / call |

## Usage

In addition to the packaged methods, this package also exposes a PostalAddress class 
that can be used to manage prefecture/city/town information. 

```
sample_location = PostalAddress("6008001")
# 京都府京都市下京区真町
sample_location.update(
  {
    "pref": "東京都",
    "pref_kana": "ﾄｳｷｮｳﾄ",
  }
)
sample_location.address
# 東京都京都市下京区真町
```

Initialization takes in both postal code and address, and you can pass custom attributes directly during initialization.
```
sample_location = PostalAddress("6008001")
sample_location = PostalAddress("埼玉県さいたま市大宮区宮町")
# custom
sample_location = PostalAddress("1020075",
  {
    "street": "6-16",
    "building": "二松学舎大学 九段1・2号館",
    "street_kana": "6-16ﾆｼｮｳｶﾞｸｼｬﾀﾞｲｶﾞｸ",
    "building_kana": "ｸﾀﾞﾝ1･2ｺﾞｳｶﾝ"
  }
)
```
You could even overwrite the kana fields with english:
```
location_en_kana = PostalAddress("1110032", 
  {
    "pref_kana": "Tokyo-To ",
    "city_kana": "Taito-Ku ",
    "town_kana": "Asakusa ",
    "street_kana":
    "2 Chome-3-1"
  }
)
location_en_kana.kana
# Tokyo-To Taito-Ku Asakusa 2 Chome-3-1
```

---

メソッドに加えて、PostalAddressで都道府県・市区町村・町域など情報を取得・調整できます。

```
sample_location = PostalAddress("6008001")
# 京都府京都市下京区真町
sample_location.update(
  {
    "pref": "東京都",
    "pref_kana": "ﾄｳｷｮｳﾄ",
  }
)
sample_location.address
# 東京都京都市下京区真町
```
郵便番号および住所から初期化できます。また、カスタム項目（都道府県・市区町村・町域など）を指定して初期化することも可能です。
```
sample_location = PostalAddress("6008001")
sample_location = PostalAddress("埼玉県さいたま市大宮区宮町")
# カスタム
sample_location = PostalAddress("1020075",
  {
    "street": "6-16",
    "building": "二松学舎大学 九段1・2号館",
    "street_kana": "6-16ﾆｼｮｳｶﾞｸｼｬﾀﾞｲｶﾞｸ",
    "building_kana": "ｸﾀﾞﾝ1･2ｺﾞｳｶﾝ"
  }
)
```
カナのプロパティを英語で上書きしてしまってもいいですよ。
```
location_en_kana = PostalAddress("1110032", 
  {
    "pref_kana": "Tokyo-To ",
    "city_kana": "Taito-Ku ",
    "town_kana": "Asakusa ",
    "street_kana":　"2 Chome-3-1"
  }
)
location_en_kana.kana
# Tokyo-To Taito-Ku Asakusa 2 Chome-3-1
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