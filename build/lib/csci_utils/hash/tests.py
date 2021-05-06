from csci_utils.hash.hash_str import hash_str, get_csci_salt
from unittest import TestCase
from unittest import mock


class HashTests(TestCase):
    def test_basic(self):
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")

    def test_get_csci_salt(self):
        with mock.patch.dict("os.environ", {"CSCI_SALT": "1a2b"}):
            self.assertEqual(get_csci_salt(), b"\x1a+")

    def test_no_Value(self):
        self.assertEqual(hash_str("", salt="").hex()[:6], "e3b0c4")
