// This module defines tests for the PostalAddress class.

import { PostalAddress } from "../models";

function testInitAutoCustom() {
  const postalBase = new PostalAddress("6008001");
}

function testResetUpdateCustomFields() {
  // ６１４－８０７７
  const postalUpdateCustom = new PostalAddress("１０５－００２２");
}

function testPartiallyInvalidPostalCodes() {
  const addr1 = new PostalAddress("1059999", {"street": "何", "building": "小島ビル"});
}

testInitAutoCustom();
testResetUpdateCustomFields();
testPartiallyInvalidPostalCodes();