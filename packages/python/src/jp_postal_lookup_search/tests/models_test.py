from jp_postal_lookup_search.models import PostalAddress

def test_init_auto_custom():
  postal_base = PostalAddress("6008001")
  assert postal_base.address == "京都府京都市下京区真町"
  assert postal_base.pref == "京都府"
  assert postal_base.city == "京都市下京区"
  assert postal_base.town == "真町"
  assert postal_base.kana == "ｷｮｳﾄﾌｷｮｳﾄｼｼﾓｷﾞｮｳｸｼﾝﾁｮｳ"
  postal_base.update({})
  postal_base.reload()
  assert postal_base.address == "京都府京都市下京区真町"
  assert postal_base.kana == "ｷｮｳﾄﾌｷｮｳﾄｼｼﾓｷﾞｮｳｸｼﾝﾁｮｳ"

  postal_street_building = PostalAddress(
    "1020075",
    {
      "street": "6-16",
      "building": "二松学舎大学 九段1・2号館",
      "street_kana": "6-16ﾆｼｮｳｶﾞｸｼｬﾀﾞｲｶﾞｸ",
      "building_kana": "ｸﾀﾞﾝ1･2ｺﾞｳｶﾝ"
    }
  )
  assert postal_street_building.address == "東京都千代田区三番町6-16二松学舎大学 九段1・2号館"
  assert postal_street_building.kana == "ﾄｳｷｮｳﾄﾁﾖﾀﾞｸｻﾝﾊﾞﾝﾁｮｳ6-16ﾆｼｮｳｶﾞｸｼｬﾀﾞｲｶﾞｸｸﾀﾞﾝ1･2ｺﾞｳｶﾝ"

  postal_en_param = PostalAddress("1110032", {"pref_kana": "Tokyo-To ", "city_kana": "Taito-Ku ", "town_kana": "Asakusa ", "street_kana": "2 Chome-3-1"})
  assert postal_en_param.address == "東京都台東区浅草"
  assert postal_en_param.kana == "Tokyo-To Taito-Ku Asakusa 2 Chome-3-1"
  postal_en_param.reload()
  assert postal_en_param.kana == "Tokyo-To Taito-Ku Asakusa 2 Chome-3-1"

  addr_base = PostalAddress("埼玉県さいたま市大宮区宮町")
  assert addr_base.postal_code == "3300802"
  assert addr_base.pref == "埼玉県"
  assert addr_base.city == "さいたま市大宮区"
  assert addr_base.town == "宮町"
  assert addr_base.kana == "ｻｲﾀﾏｹﾝｻｲﾀﾏｼｵｵﾐﾔｸﾐﾔﾁｮｳ"

  addr_chome = PostalAddress("北海道札幌市中央区北一条西９丁目")
  assert addr_chome.address == "北海道札幌市中央区北一条西（１～１９丁目）"
  assert addr_chome.kana == "ﾎｯｶｲﾄﾞｳｻｯﾎﾟﾛｼﾁｭｳｵｳｸｷﾀ1ｼﾞｮｳﾆｼ(1-19ﾁｮｳﾒ)"

def test_reset_update_custom_fields():
  # ６１４－８０７７
  postal_update_custom = PostalAddress("１０５－００２２")
  postal_update_custom.update(
    {
      "pref": "京都",
      "city": "府八幡市",
      "pref_kana": "ｷｮｳﾄ",
      "city_kana": "ﾌﾔﾜﾀｼ"
    }
  )
  print(postal_update_custom.address)
  print(postal_update_custom.kana)
  postal_update_custom.update({}
  )
  print(postal_update_custom.address)
  print(postal_update_custom.kana)

def test_partially_invalid_postal_codes():
  addr_1 = PostalAddress("1059999", {"street": "何", "building": "小島ビル"})
  assert addr_1.address == "東京都何小島ビル"
  assert addr_1.kana == "ﾄｳｷｮｳﾄ"
  addr_1.set_postal("9990232")
  addr_1.reload()
  assert addr_1.address == "山形県何小島ビル"
  assert addr_1.kana == "ﾔﾏｶﾞﾀｹﾝ"

if __name__ == "__main__":
  test_init_auto_custom()
  test_reset_update_custom_fields()
  test_partially_invalid_postal_codes()