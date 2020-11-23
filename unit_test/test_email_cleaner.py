import eml_parser.email_cleaner as EmailCleaner
from unittest import TestCase


class TestEmailCleaner(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_email_as_list(self):
        actual = EmailCleaner.get_emails_as_list(
            "//example@findme.com sometext bob@test.com somemore text <>!@#$%^ <bob@test2.com> 12341234"
        )
        self.assertEqual(actual[0], "example@findme.com")
        self.assertEqual(actual[1], "bob@test.com")
        self.assertEqual(actual[2], "bob@test2.com")

    def test_get_emails_as_string(self):
        actual = EmailCleaner.get_emails_as_string(
            "//example@findme.com sometext bob@test.com somemore text <>!@#$%^ <bob@test2.com> 12341234"
        )
        self.assertEqual(actual, "example@findme.com, bob@test.com, bob@test2.com")

    def test_recipient_bug(self):
        actual = EmailCleaner.get_emails_as_list(
            '        {          "key": "To",          "value": "Test.User@example.com"        }'
        )
        expected = ["Test.User@example.com"]
        self.assertEqual(actual, expected)

    def test_recipient_bug_2(self):
        actual = EmailCleaner.get_emails_as_list(
            '        {          "key": "To",          "value": "A.B.C.D.User@example.A.B.C.com"        }'
        )
        expected = ["A.B.C.D.User@example.A.B.C.com"]
        self.assertEqual(actual, expected)

    def test_get_email_as_list_blank_list(self):
        actual = EmailCleaner.get_emails_as_list("")
        self.assertEqual(actual, [])
