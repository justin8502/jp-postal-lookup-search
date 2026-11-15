"""This module defines tests for find methods."""

import re
import time
from jp_postal_lookup_search.find import (
  lookup_address_by_postal_code,
  lookup_address_parts_by_postal_code,
  lookup_address_kana_by_postal_code,
  search_postal_code_by_address,
)

def test_bulk_postal_lookup():
  postal_codes = ["1000001", "1050022", "1500001", "1600022", "1060032", "2200011",
                  "2310011", "3300802", "2730005", "6008001", "6048006", "5300001", 
                  "5420081", "6500021", "4600008", "4500002", "8100001", "7300031", 
                  "9800021", "0600001", "9000015"]
  
  for postal_code in postal_codes:
    address_lookup = lookup_address_by_postal_code(postal_code)
    postal_lookup = search_postal_code_by_address(address_lookup)
    assert postal_lookup == postal_code, (
      f"Mismatch for {postal_code}: "
      f"expected {postal_code}, got {postal_lookup}"
    )

def test_postal_lookup_parts():
  postal_codes = ["1500001", "3300802", "4500002"]

  for postal_code in postal_codes:
    address_lookup = lookup_address_by_postal_code(postal_code)
    address_lookup_parts = lookup_address_parts_by_postal_code(postal_code)

    address_lookup_parts_str = "".join([
      address_lookup_parts["pref"],
      address_lookup_parts["city"],
      address_lookup_parts["town"]
    ])
    assert address_lookup == address_lookup_parts_str, (
      f"Mismatch for {postal_code}: "
      f"expected {address_lookup}, got {address_lookup_parts_str}"
    )

def test_postal_lookup_kana():
  postal_codes = ["1500001", "3300802", "2730005"]
  lookup_kana = ["ﾄｳｷｮｳﾄｼﾌﾞﾔｸｼﾞﾝｸﾞｳﾏｴ", "ｻｲﾀﾏｹﾝｻｲﾀﾏｼｵｵﾐﾔｸﾐﾔﾁｮｳ", "ﾁﾊﾞｹﾝﾌﾅﾊﾞｼｼﾎﾝﾁｮｳ"]
  
  for postal_code, kana in zip(postal_codes, lookup_kana):
    address_lookup_kana = lookup_address_kana_by_postal_code(postal_code)
    assert address_lookup_kana == kana, (
      f"Mismatch for {postal_code}: "
      f"expected {kana}, got {address_lookup_kana}"
    )

def test_postal_lookup_normalization():
  postal_codes = [
    "1500001",
    "150-0001",
    "１５００００１",
    "１５０ー０００１",
    "〒１５００００１",
  ]

  base_postal_code = "1500001"
  
  for postal_code in postal_codes:
    address_lookup = lookup_address_by_postal_code(postal_code)
    postal_lookup = search_postal_code_by_address(address_lookup)
    assert postal_lookup == base_postal_code, (
      f"Mismatch for {postal_code}: "
      f"expected {base_postal_code}, got {postal_lookup} for {postal_code}"
    )

def test_fuzzy_matching():
  # テキスト正規化
  # 東京都港区赤坂（次のビルを除く）
  tokyo_text_variance = ["東京都港区赤坂1丁目10-5", "東京都港区赤坂１丁目ー１０-５", "東京都港区赤坂1丁目10-5藤田ビル"]
  tokyo_text_variance_postal = "1070052"

  for tokyo_addr in tokyo_text_variance:
    postal_lookup = search_postal_code_by_address(tokyo_addr)
    assert postal_lookup == tokyo_text_variance_postal, (
      f"Mismatch for {tokyo_addr}: "
      f"expected {tokyo_text_variance_postal}, got {postal_lookup}"
    )

  # 丁目マッチング
  # 宮崎県日南市吾田東（５～１１丁目）
  miyazaki_nichinan_agatahigashi_postal = "8892541"
  miyazaki_nichinan_agatahigashi_chome = ["宮崎県日南市吾田東５丁目", "宮崎県日南市吾田東６丁目", "宮崎県日南市吾田東７丁目ー１ー２"]
  for miyazaki_addr in miyazaki_nichinan_agatahigashi_chome:
    postal_lookup = search_postal_code_by_address(miyazaki_addr)
    assert miyazaki_nichinan_agatahigashi_postal == postal_lookup, (
      f"Mismatch for {miyazaki_addr}: "
      f"expected {miyazaki_nichinan_agatahigashi_postal}, got {postal_lookup}"
    )

  # 北海道札幌市中央区北一条西（１～１９丁目）
  hokkaido_fuzzy_postal = "0600001"
  hokkaido_fuzzy = ["北海道札幌市中央区北一条西９丁目", "北海道札幌市中央区北一条西１4丁目", "北海道札幌市中央区北一条西１９丁目"]
  
  for hokkaido_addr in hokkaido_fuzzy:
    postal_lookup = search_postal_code_by_address(hokkaido_addr)
    assert hokkaido_fuzzy_postal == postal_lookup, (
      f"Mismatch for {hokkaido_addr}: "
      f"expected {hokkaido_fuzzy_postal}, got {postal_lookup}"
    )

def test_special_cases():
  # 一円
  # 長野県北安曇郡松川村松川村一円
  ichien_address = "長野県北安曇郡松川村松川村一円"
  postal_lookup = search_postal_code_by_address(ichien_address)
  ichien_address_short = "長野県北安曇郡松川村松川村"
  postal_lookup_short = search_postal_code_by_address(ichien_address_short)
  assert postal_lookup == "3998501"
  assert postal_lookup == postal_lookup_short

  # その他
  tokyo_shinjuku_other = "東京都新宿区戸山公園"
  postal_lookup = search_postal_code_by_address(tokyo_shinjuku_other)
  assert postal_lookup == "1620052"

  # 以下に掲載がない場合
  fukuoka_koge_other = "福岡県築上郡上毛町近所医者"
  postal_lookup = search_postal_code_by_address(fukuoka_koge_other)
  assert postal_lookup == "8710900"

def benchmark_lookup_find():
  postal_codes = ["1000001", "1050022", "1500001", "1600022", "1060032", "2200011", 
                  "2310011", "3300802", "2730005", "6008001"]

  addresses = ["東京都千代田区千代田", "東京都港区海岸（１、２丁目）", "東京都渋谷区神宮前",
               "東京都新宿区新宿", "東京都港区六本木（次のビルを除く）", "神奈川県横浜市西区高島",
               "神奈川県横浜市中区太田町", "埼玉県さいたま市大宮区宮町", "千葉県船橋市本町",
               "京都府京都市下京区真町"]

  # perform 10000 postal code/part/kana lookups
  print_benchmark_tests(lookup_address_by_postal_code, postal_codes)
  print_benchmark_tests(lookup_address_parts_by_postal_code, postal_codes)
  print_benchmark_tests(lookup_address_kana_by_postal_code, postal_codes)

  # perform 10000 searches
  print_benchmark_tests(search_postal_code_by_address, addresses)

  # perform 10000 lookups/searches
  print_benchmark_tests(
    lambda postal_code: search_postal_code_by_address(
      lookup_address_by_postal_code(postal_code)
    ),
    postal_codes,
    name="search_postal_code_by_address + lookup_address_by_postal_code"
  )

def test_invalid_input():
  invalid_postal_1 = "0000000"
  invalid_postal_2 = "0101010"
  invalid_address_1 = "東京都沖縄"
  invalid_address_2 = "50 Hudson Yards, New York, NY 10001, United States"

  invalid_lookup_pref_text = "都道府県情報を検索できません。"
  invalid_lookup_text = "住所情報を検索できません。"
  invalid_search_text = "郵便番号を検索できません。検索ステージ：ST"

  postal_lookup = lookup_address_by_postal_code(invalid_postal_1)
  assert postal_lookup == invalid_lookup_pref_text

  postal_lookup = lookup_address_by_postal_code(invalid_postal_2)
  assert postal_lookup == invalid_lookup_text

  address_lookup = search_postal_code_by_address(invalid_address_1)
  assert address_lookup == re.sub("ST", "市区町村", invalid_search_text)

  address_lookup = search_postal_code_by_address(invalid_address_2)
  assert address_lookup == re.sub("ST", "都道府県", invalid_search_text)

def print_benchmark_tests(func, inputs, name=None):
  t_lookup_st = time.time()
  for _ in range(1000):
    for input in inputs:
      func(input)
  t_lookup_end = time.time()
  elapsed_ms_per_call = (t_lookup_end - t_lookup_st) / 10
  print(f"{name or func.__name__}: {elapsed_ms_per_call:.6f} ms/call")

if __name__ == "__main__":
  # Since most of the checks are against static values, it is possible they could fail
  # if the dataset is updated. However, it is still a good benchmark.
  test_bulk_postal_lookup()
  test_postal_lookup_parts()
  test_postal_lookup_kana()
  test_postal_lookup_normalization()
  test_fuzzy_matching()
  test_special_cases()
  test_invalid_input()
  benchmark_lookup_find()