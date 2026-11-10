from jp_postal_lookup_search.find import (
  lookup_address_by_postal_code,
  lookup_address_by_postal_code_kana,
  search_postal_code_by_address,
)

def test_postal_lookup():
  postal_codes = ["1000001", "1050022", "1500001", "1600022", "1060032", "2200011", 
                  "2310011", "3300802", "2730005", "6008001", "6048006", "5300001", 
                  "5420081", "6500021", "4600008", "4500002", "8100001", "7300031", 
                  "9800021", "0600001", "9000015"]
  
  for postal_code in postal_codes:
    address_lookup = lookup_address_by_postal_code(postal_code)
    postal_lookup = search_postal_code_by_address(address_lookup)
    assert postal_lookup == postal_code

  # address_lookup = lookup_address_by_postal_code(postal_code)
  postal_lookup = search_postal_code_by_address("北海道札幌市中央区北一条西１4丁目")
  assert postal_lookup == "0600001"
  postal_lookup = search_postal_code_by_address("東京都港区赤坂1丁目10-5")
  assert postal_lookup == "1070052"
  address_lookup = lookup_address_by_postal_code("0691214")
  postal_lookup = search_postal_code_by_address(address_lookup)
  ichien = search_postal_code_by_address("長野県北安曇郡松川村松川村一円")
  print(ichien)
  ichien = search_postal_code_by_address("長野県北安曇郡松川村")
  print(ichien)
  special = search_postal_code_by_address("静岡県磐田市大原（１番地～２０６１番地、２７５７番地～２７６８番地）")
  print(special)
  special = search_postal_code_by_address("静岡県磐田市大原2000番地")
  print(special)
  shiba = search_postal_code_by_address("東京都港区海岸１丁目ー５ー４")
  print(shiba)
  shiba = search_postal_code_by_address("東京都港区海岸1丁目ー5ー4")
  print(shiba)

if __name__ == "__main__":
  test_postal_lookup()