import re
import time
from jp_postal_lookup_search.models import PostalAddress

def test_init_auto_custom():
  addr_1 = PostalAddress("1059999", {"street": "何", "building": "小島ビル"})
  assert addr_1.kana == "ﾄｳｷｮｳﾄ"
  assert addr_1.addr == "東京都何小島ビル"
  addr_1.set_postal("9990232")
  addr_1.reload()
  assert addr_1.kana == "ﾔﾏｶﾞﾀｹﾝ"
  assert addr_1.addr == "山形県何小島ビル"

if __name__ == "__main__":
  test_init_auto_custom()