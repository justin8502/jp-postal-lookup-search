// This module defines tests for the PostalAddress class.

import { PostalAddress } from "../models";
import { assert } from "../utils";

function testInitAutoCustom() {
  const postalBase = new PostalAddress("6008001");
  assert(postalBase.getAddress() === "京都府京都市下京区真町");
  assert(postalBase.pref === "京都府");
  assert(postalBase.city === "京都市下京区");
  assert(postalBase.town === "真町");
  assert(postalBase.getKana() === "ｷｮｳﾄﾌｷｮｳﾄｼｼﾓｷﾞｮｳｸｼﾝﾁｮｳ");
  postalBase.updateCustom({});
  postalBase.reload();
  assert(postalBase.getAddress() === "京都府京都市下京区真町");
  assert(postalBase.getKana() === "ｷｮｳﾄﾌｷｮｳﾄｼｼﾓｷﾞｮｳｸｼﾝﾁｮｳ");

  const postalStreetBuilding = new PostalAddress(
    "1020075",
    {
      "street": "6-16",
      "building": "二松学舎大学 九段1・2号館",
      "streetKana": "6-16ﾆｼｮｳｶﾞｸｼｬﾀﾞｲｶﾞｸ",
      "buildingKana": "ｸﾀﾞﾝ1･2ｺﾞｳｶﾝ"
    }
  );
  assert(postalStreetBuilding.getAddress() === "東京都千代田区三番町6-16二松学舎大学 九段1・2号館");
  assert(postalStreetBuilding.getKana() === "ﾄｳｷｮｳﾄﾁﾖﾀﾞｸｻﾝﾊﾞﾝﾁｮｳ6-16ﾆｼｮｳｶﾞｸｼｬﾀﾞｲｶﾞｸｸﾀﾞﾝ1･2ｺﾞｳｶﾝ");

  const postalEnParam = new PostalAddress("1110032", {"prefKana": "Tokyo-To ", "cityKana": "Taito-Ku ", "townKana": "Asakusa ", "streetKana": "2 Chome-3-1"});
  assert(postalEnParam.getAddress() === "東京都台東区浅草");
  assert(postalEnParam.getKana() === "Tokyo-To Taito-Ku Asakusa 2 Chome-3-1");
  postalEnParam.reload();
  assert(postalEnParam.getKana() === "Tokyo-To Taito-Ku Asakusa 2 Chome-3-1");

  const addrBase = new PostalAddress("埼玉県さいたま市大宮区宮町");
  assert(addrBase.getPostalCode() === "3300802");
  assert(addrBase.pref === "埼玉県");
  assert(addrBase.city === "さいたま市大宮区");
  assert(addrBase.town === "宮町");
  assert(addrBase.getKana() === "ｻｲﾀﾏｹﾝｻｲﾀﾏｼｵｵﾐﾔｸﾐﾔﾁｮｳ");

  const addrChome = new PostalAddress("北海道札幌市中央区北一条西９丁目");
  assert(addrChome.getAddress() === "北海道札幌市中央区北一条西（１～１９丁目）");
  assert(addrChome.getKana() === "ﾎｯｶｲﾄﾞｳｻｯﾎﾟﾛｼﾁｭｳｵｳｸｷﾀ1ｼﾞｮｳﾆｼ(1-19ﾁｮｳﾒ)");

  console.log("testInitAutoCustom: OK");
}

function testResetUpdateCustomFields() {
  // ６１４－８０７７
  const postalUpdateCustom = new PostalAddress("１０５－００２２");
  postalUpdateCustom.updateCustom({
    "pref": "京都",
    "city": "府八幡市",
    "prefKana": "ｷｮｳﾄ",
    "cityKana": "ﾌﾔﾜﾀｼ"
  });
  assert(postalUpdateCustom.getAddress() === "京都府八幡市海岸（１、２丁目）");
  assert(postalUpdateCustom.getKana() === "ｷｮｳﾄﾌﾔﾜﾀｼｶｲｶﾞﾝ(1､2ﾁｮｳﾒ)");
  postalUpdateCustom.updateCustom({});
  assert(postalUpdateCustom.getAddress() === "東京都港区海岸（１、２丁目）");
  assert(postalUpdateCustom.getKana() === "ﾄｳｷｮｳﾄﾐﾅﾄｸｶｲｶﾞﾝ(1､2ﾁｮｳﾒ)");

  console.log("testResetUpdateCustomFields: OK");
}

function testPartiallyInvalidPostalCodes() {
  const addr1 = new PostalAddress("1059999", {"street": "何", "building": "小島ビル"});
  assert(addr1.getAddress() === "東京都何小島ビル");
  assert(addr1.getKana() === "ﾄｳｷｮｳﾄ");
  addr1.setPostal("9990232");
  addr1.reload();
  assert(addr1.getAddress() === "山形県何小島ビル");
  assert(addr1.getKana() === "ﾔﾏｶﾞﾀｹﾝ");

  console.log("testPartiallyInvalidPostalCodes: OK");
}

function testPostalAddressEquality() {
  const addr1 = new PostalAddress("6008001", {"street": "何", "building": "小島ビル"});
  const addr2 = new PostalAddress("6008001");
  const addr3 = new PostalAddress("１０５－００２２", {"street": "何", "building": "小島ビル"});
  addr1.update({
    town: "○○町"
  })

  assert(addr1.equals(addr2));
  assert(!addr1.strictEquals(addr2));
  assert(!addr1.equals(addr3));

  console.log("testPostalAddressEquality: OK");
}

testInitAutoCustom();
testResetUpdateCustomFields();
testPartiallyInvalidPostalCodes();
testPostalAddressEquality();