from jp_postal_lookup_search.find import (
  lookup_address_by_postal_code,
  lookup_address_by_postal_code_kana,
  search_postal_code_by_address,
)

def test_postal_lookup():
    result = lookup_address_by_postal_code("1050022")
    assert result is not None
    result2 = lookup_address_by_postal_code_kana("1050022")
    print(result2)
    print(result)
    print(search_postal_code_by_address("東京都港区海岸（１、２丁目）"))
    print(search_postal_code_by_address("北海道札幌市中央区"))


if __name__ == "__main__":
    test_postal_lookup()