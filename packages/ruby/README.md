# JP Postal Lookup Search

※日本語版が続きます

A project that allows lookups/searches based on japanese addresses and postal codes. 
Functionality and dataset is built around the official Japan Post ken_all dataset. 

Supports partial/incomplete matching, local overrides (see usage). 

Example:
```rb
```

---

このプロジェクトでは、郵便番号から住所を検索したり、住所から郵便番号を検索したりできます。
日本郵便の公式サイトで公開されている郵便番号データ（KEN_ALL）を使用しています。

部分一致・不完全な住所での検索や、ローカルでの上書き設定にも対応しています（Usageを参照）。

例：
```rb
```

## Methods

| Method / 関数 | Description / 説明 | Example / 例 | Speed / 速度 |
|---|---|---|---|

## Usage

Installation
```
```
Importing methods & PostalAddress class
```rb
```

In addition to the packaged methods, this package also exposes a PostalAddress class 
that can be used to manage prefecture/city/town information. 

```rb
```

Initialization takes in both postal code and address, and you can pass custom attributes directly during initialization.

```rb
```

You could even overwrite the kana fields with english:

```rb
```

---

インストール
```
```
関数および PostalAddress クラスのインポート
```rb
```

メソッドに加えて、PostalAddressで都道府県・市区町村・町域など情報を取得・調整できます。

```rb
```

郵便番号および住所から初期化できます。また、カスタム項目（都道府県・市区町村・町域など）を指定して初期化することも可能です。

```rb
```

カナのプロパティを英語で上書きしてしまってもいいですよ。

```rb
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