"""Unit tests using only Python's standard library."""

import unittest

from study_app import check_answer, make_password_hash, normalize_answer, valid_password, valid_username


class StudyAppTests(unittest.TestCase):
    def test_username_length_and_uniqueness(self):
        self.assertTrue(valid_username("student1", {}))
        self.assertFalse(valid_username("abc", {}))
        self.assertFalse(valid_username("verylongname", {}))
        self.assertFalse(valid_username("student1", {"student1": object()}))

    def test_password_rules(self):
        self.assertTrue(valid_password("Hello123"))
        self.assertFalse(valid_password("abc"))
        self.assertFalse(valid_password("abcd!"))
        self.assertFalse(valid_password("пароль123"))
        self.assertFalse(valid_password("abc 12"))

    def test_answers(self):
        self.assertEqual(normalize_answer("  КЕРЕЙ ХАН "), "керей хан")
        self.assertTrue(check_answer(" 1991 ГОД ", "1991 год"))
        self.assertFalse(check_answer("1992", "1991"))

    def test_hash_deterministic_with_same_salt(self):
        self.assertEqual(make_password_hash("abcde", b"0" * 16), make_password_hash("abcde", b"0" * 16))
        self.assertNotEqual(make_password_hash("abcde", b"0" * 16), make_password_hash("abcdf", b"0" * 16))


if __name__ == "__main__":
    unittest.main()
