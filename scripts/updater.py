import csv
import json
import os
from requests import get
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile

def split_postal_address(addr: str):
    return [addr[0:3], addr[3:]]

ken_all_url = get('https://www.post.japanpost.jp/service/search/zipcode/download/kogaki/zip/ken_all.zip')
zip_file = ZipFile(BytesIO(ken_all_url.content))
files = zip_file.namelist()

postal_code_map = {}
city_town_code_map = {}
with zip_file.open(files[0], 'r') as raw_content:
    jp_encoded_file = TextIOWrapper(raw_content, encoding='cp932', newline='')
    csvreader = csv.reader(jp_encoded_file)
    for row in csvreader:
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
            town_has_two_postal_codes,
            street_refers_to_district,
            street_names,
            postal_code_has_two_plus_towns,
            updated,
            address_change_reason
        ) = row

        prefecture_code, city_town_code = split_postal_address(postal_code)

        if prefecture_code not in postal_code_map:
            postal_code_map[prefecture_code] = {
                # Concat into single strings to reduce json size
                "prefecture": f"{prefecture_name}|{prefecture_kata}",
                city_town_code: f"{city_name}|{town_name}|{city_kata}|{town_kata}"
            }
        else:
            postal_code_map[prefecture_code][city_town_code] = f"{city_name}|{town_name}|{city_kata}|{town_kata}"

# TODO: Tests
# print(postal_code_map["111"]["prefecture"] + postal_code_map["111"]["0041"])
# print(postal_code_map["111"]["prefecture_kata"] + postal_code_map["111"]["0041"]["city_kata"] + postal_code_map["111"]["0041"]["town_kata"])

script_dir = os.path.dirname(__file__)
# turn off ensure_ascii and newline to reduce file size
with open(os.path.join(script_dir, "../json/postal_codes.json"), 'w', encoding="utf-8") as fp:
    json.dump(
        postal_code_map,
        fp,
        ensure_ascii=False,
        separators=(",", ":")
    )