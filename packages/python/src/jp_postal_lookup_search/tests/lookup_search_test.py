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

if __name__ == "__main__":
  test_postal_lookup()