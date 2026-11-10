# JP Postal Lookup Search
※日本語版が続きます

A project that allows lookups/searches based on japanese addresses and postal codes. 
Functionality and dataset is built around the official Japan Post ken_all dataset. 

Example:
```
lookup_address_by_postal_code("6500021") -> "兵庫県神戸市中央区三宮町"
search_postal_code_by_address("兵庫県神戸市中央区三宮町") -> "6500021"
```

Also supports partial/incomplete matching, local overrides (see usage). 

---

このプロジェクトでは、郵便番号から住所を検索したり、住所から郵便番号を検索したりできます。
日本郵便の公式サイトで公開されている郵便番号データ（KEN_ALL）を使用しています。

例：
```
lookup_address_by_postal_code("6500021") -> "兵庫県神戸市中央区三宮町"
search_postal_code_by_address("兵庫県神戸市中央区三宮町") -> "6500021"
```

部分一致・不完全な住所での検索や、ローカルでの上書き設定にも対応しています（Usageを参照）。

## Methods

| Method / 関数 | Description / 説明 | Example / 例 |
|---|---|---|
| `lookup_address_by_postal_code(postal_code)` | Looks up address associated with postal code / 郵便番号から住所を検索します。 | `lookup_address_by_postal_code("6500021")` |
| `lookup_address_by_postal_code_kana(postal_code)` | Looks up address (in kana) associated with postal code / 郵便番号から住所のカナ表記を検索します。 | `lookup_address_by_postal_code_kana("6500021")` |
| `search_postal_code_by_address(address)` | Matches address to a postal code / 住所から郵便番号を検索します。 | `search_postal_code_by_address("兵庫県神戸市中央区三宮町")` |

## Usage

## Development

The development of this project is guided by 4 principles:
1. No callbacks. Everything should be synchronous
2. Reduce/Eliminate external dependencies
3. Emphasize usability and extensibility
4. Keep static files small in size

---

このプロジェクトの実装中心点は以下になります：
1. コールバック関数厳禁
2. 依存パッケージなし
3. 使いやすさと拡張性を重視
4. 必要ファイル量減少

## Future Goals

EN Support, Github Actions Automatic Update/Build