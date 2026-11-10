import csv
import json
import os
from typing import Dict
from requests import get
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
from dataclasses import dataclass

type PostalMapEntry = dict[str, int]

@dataclass
class AddressMapEntry:
  city: Dict[str, int]

def split_postal_address(addr: str) -> tuple[str, str]:
  return addr[0:3], addr[3:]

def merge_existing(existing: str, new: str) -> str:
  # split and recombine existing data
  existing_city_name, existing_town_name, existing_city_kata, existing_town_kata = existing.split("|")
  _new_city_name, new_town_name, _new_city_kata, new_town_kata = new.split("|")

  if existing_town_name == "以下に掲載がない場合": return existing

  return "|".join([
    existing_city_name,
    existing_town_name + new_town_name,
    existing_city_kata,
    existing_town_kata + new_town_kata
  ])

def dedupe_address_map(address_map):
  for prefecture, cities in address_map.items():
    for city, towns in cities.items():
      dedupe_town_map = {}

      for key, code in sorted(
        towns.items(),
        key=lambda item: len(item[0]),
        reverse=True
      ):
        if code not in dedupe_town_map.values():
          dedupe_town_map[key] = code

      address_map[prefecture][city] = dedupe_town_map

  return address_map

def extract_row(row: list[str], postal_code_map: Dict[str, PostalMapEntry], address_map: Dict[str, AddressMapEntry]) -> None:
  # 全国地方公共団体コード（JIS X0401、X0402）………　半角数字
  # （旧）郵便番号（5桁）………………………………………　半角数字
  # 郵便番号（7桁）………………………………………　半角数字
  # 都道府県名　…………　半角カタカナ（コード順に掲載）　（※1）
  # 市区町村名　…………　半角カタカナ（コード順に掲載）　（※1）
  # 町域名　………………　半角カタカナ（五十音順掲載）　（※1）
  # 都道府県名　…………　漢字（コード順に掲載）　（※1,2）
  # 市区町村名　…………　漢字（コード順に掲載）　（※1,2）
  # 町域名　………………　漢字（五十音順に掲載）　に（※1,2）
  # 一町域が二以上の郵便番号で表される場合の表示　（※3）　（「1」は該当、「0」は該当せず）
  # 小字毎に番地が起番されている町域の表示　（※4）　（「1」は該当、「0」は該当せず）
  # 丁目を有する町域の場合の表示　（「1」は該当、「0」は該当せず）
  # 一つの郵便番号で二以上の町域を表す場合の表示　（※5）　（「1」は該当、「0」は該当せず）
  # 更新の表示（※6）（「0」は変更なし、「1」は変更あり、「2」廃止（廃止データのみ使用））
  # 変更理由　（「0」は変更なし、「1」市政・区政・町政・分区・政令指定都市施行、「2」住居表示の実施、「3」区画整理、「4」郵便区調整等、「5」訂正、「6」廃止（廃止データのみ使用））
  (
    _nat_gov_code,
    _old_postal_code,
    postal_code,
    prefecture_kata,
    city_kata,
    town_kata,
    prefecture_name,
    city_name,
    town_name,
    _town_has_two_postal_codes,
    _street_refers_to_district,
    _street_names,
    _postal_code_has_two_plus_towns,
    _recently_updated,
    _address_change_reason
  ) = row

  prefecture_code, city_town_code = split_postal_address(postal_code)

  # Concat into single strings to reduce json size
  prefecture_condensed = f"{prefecture_name}|{prefecture_kata}"
  city_town_condensed = f"{city_name}|{town_name}|{city_kata}|{town_kata}"

  pref = postal_code_map.setdefault(prefecture_code, {
    "prefecture": prefecture_condensed
  })

  if city_town_code in pref:
    pref[city_town_code] = merge_existing(
      pref[city_town_code], city_town_condensed
    )
  else:
    pref[city_town_code] = city_town_condensed

  recombined_town_key = pref[city_town_code].split("|")[1]

  address_map.setdefault(prefecture_name, {}) \
             .setdefault(city_name, {})[recombined_town_key] = postal_code

def fetch_and_populate_maps() -> tuple[Dict[str, PostalMapEntry], Dict[str, AddressMapEntry]]:
  ken_all_url = get('https://www.post.japanpost.jp/service/search/zipcode/download/kogaki/zip/ken_all.zip')
  zip_file = ZipFile(BytesIO(ken_all_url.content))
  files = zip_file.namelist()

  postal_code_map = {}
  address_map = {}
  with zip_file.open(files[0], 'r') as raw_content:
    jp_encoded_file = TextIOWrapper(raw_content, encoding='cp932', newline='')
    csvreader = csv.reader(jp_encoded_file)
    for row in csvreader:
      extract_row(row, postal_code_map, address_map)

  return [postal_code_map, address_map]

def validate_data(postal_code_map: Dict[str, PostalMapEntry], address_map: Dict[str, AddressMapEntry]) -> None:
  assert postal_code_map, "Postal code map is empty"
  assert address_map, "Address map is empty"

  prefectures = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
  ]

  postal_code_map_tests = {
    "1050022": "東京都|ﾄｳｷｮｳﾄ",
    "9030129": "沖縄県|ｵｷﾅﾜｹﾝ",
    "0700034": "北海道|ﾎｯｶｲﾄﾞｳ"
  }

  assert set(prefectures) == set(address_map.keys()), "Prefecture keys do not match"

  for postal_code in postal_code_map_tests:
    prefecture_code, _city_town_code = split_postal_address(postal_code)
    prefecture_string = postal_code_map[prefecture_code]["prefecture"]
    assert prefecture_string == postal_code_map_tests[postal_code], (
      f"Sample lookup did not match test data: {postal_code}: {prefecture_string}"
    )

def write_to_files(postal_code_map: Dict[str, PostalMapEntry], address_map: Dict[str, AddressMapEntry]) -> None:
  script_dir = os.path.dirname(__file__)

  file_defaults = {
    "ensure_ascii": False,
    "separators": (",", ":"),
    "indent": 2,
  }

  files = {
    "postal_code_lookup.json": postal_code_map,
    "address_lookup.json": address_map,
  }

  for filename, data in files.items():
    filepath = os.path.join(script_dir, "../json", filename)

    with open(filepath, "w", encoding="utf-8") as fp:
      json.dump(data, fp, **file_defaults)

def main() -> None:
  postal_code_map, address_map = fetch_and_populate_maps()
  validate_data(postal_code_map, address_map)
  dedupe_address_map(address_map)
  write_to_files(postal_code_map, address_map)

if __name__ == "__main__":
  main()