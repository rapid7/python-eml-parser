from unittest import TestCase
from eml_parser.icon_email import IconEmail
from eml_parser.icon_file import IconFile
from eml_parser.email_parser import EmailParser
from eml_parser.exceptions import EmailParserException
from email import message_from_string
import logging
import datetime
import os

CURRENT_DIR = os.path.dirname(__file__)
BASIC_MESSAGE_PAYLOAD = (
    f"{CURRENT_DIR}/payloads/get_messages_payload_one_basic_message.json"
)
BASIC_ATTACHMENT_PAYLOAD = f"{CURRENT_DIR}/payloads/get_attachment_email_payload.json"


# Get a real payload from file
def read_file_to_string(filename):
    with open(filename) as my_file:
        return my_file.read()


class TestIconEmail(TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger("Test")
        pass

    def test_create_blank_email(self):
        email = IconEmail()
        self.assertEqual(email.id, None)
        self.assertEqual(email.recipients, None)
        self.assertEqual(email.is_read, None)
        self.assertEqual(email.sender, None)
        self.assertEqual(email.subject, None)
        self.assertEqual(email.indicators, None)

    def test_create_email(self):
        params = {
            "account": "test_account@test.com",
            "recipients": "[test@test.com]",
            "is_read": True,
            "id": "test_id",
            "sender": "someguy@test.com",
            "body": "This is some text",
            "categories": ["Foo", "Bar"],
            "date_received": "Today",
            "headers": [{"header1": "value1"}],
        }

        email = IconEmail(**params)
        self.assertEqual(email.account, "test_account@test.com")
        self.assertEqual(email.recipients, "[test@test.com]")
        self.assertEqual(email.is_read, True)
        self.assertEqual(email.id, "test_id")
        self.assertEqual(email.sender, "someguy@test.com")
        self.assertEqual(email.body, "This is some text")
        self.assertEqual(email.categories, ["Foo", "Bar"])
        self.assertEqual(email.date_received, "Today")
        self.assertEqual(email.headers, [{"header1": "value1"}])
        self.assertEqual(email.has_attachments, False)
        self.assertEqual(email.indicators.md5, "97214f63224bc1e9cc4da377aadce7c7")
        self.assertEqual(
            email.indicators.sha1, "482cb0cfcbed6740a2bcb659c9ccc22a4d27b369"
        )
        self.assertEqual(
            email.indicators.sha256,
            "2263d8dd95ccfe1ad45d732c6eaaf59b3345e6647331605cb15aae52002dff75",
        )
        self.assertEqual(email.attached_files, [])
        self.assertEqual(email.attached_emails, [])
        self.assertEqual(email.flattened_attached_emails, [])
        self.assertEqual(email.flattened_attached_files, [])

    def test_make_serializable(self):
        icon_email = IconEmail()
        actual = icon_email.make_serializable()

        expected = {
            "attached_emails": [],
            "attached_files": [],
            "flattened_attached_emails": [],
            "flattened_attached_files": [],
            "has_attachments": False,
        }

        self.assertEqual(actual, expected)

    def test_flatten(self):
        email_with_nested_attachments_text = read_file_to_string(
            f"{CURRENT_DIR}/payloads/email_with_nested_attachments_python_object.txt"
        )
        email_with_nested_attachments = eval(email_with_nested_attachments_text)

        icon_email = IconEmail(**email_with_nested_attachments)

        # This is a LOT of work to make a complex mocked object
        # At this point, before flattening...all sub emails and files should be
        # IconFiles and IconEmails respectively...thus this mass of loopiness
        for i, attached_file in enumerate(icon_email.attached_files):
            new_file = IconFile(**attached_file)
            icon_email.attached_files[i] = new_file

        for i, attached_email in enumerate(icon_email.attached_emails):
            new_email = IconEmail(**attached_email)
            icon_email.attached_emails[i] = new_email
            if len(icon_email.attached_emails[i].attached_files) > 0:
                icon_email.attached_emails[i].attached_files[0] = IconFile(
                    **icon_email.attached_emails[i].attached_files[0]
                )
            if len(icon_email.attached_emails[i].attached_emails) > 0:
                for j, sub_attached_email in enumerate(
                    icon_email.attached_emails[i].attached_emails
                ):
                    new_sub_email = IconEmail(**sub_attached_email)
                    icon_email.attached_emails[i].attached_emails[j] = new_sub_email
                    if (
                        len(
                            icon_email.attached_emails[i]
                            .attached_emails[j]
                            .attached_files
                        )
                        > 0
                    ):
                        icon_email.attached_emails[i].attached_emails[j].attached_files[
                            0
                        ] = IconFile(
                            **icon_email.attached_emails[i]
                            .attached_emails[j]
                            .attached_files[0]
                        )

        icon_email.flatten()
        self.assertEqual(icon_email.has_attachments, True)

        self.assertEqual(len(icon_email.attached_emails), 2)
        self.assertEqual(len(icon_email.attached_files), 1)

        self.assertEqual(icon_email.attached_files[0].name, "example.com")

        self.assertEqual(icon_email.attached_emails[0].subject, "Level 2 subject")
        self.assertEqual(icon_email.attached_emails[1].subject, "Pic attached")
        self.assertEqual(icon_email.subject, "level 3")

        self.assertEqual(len(icon_email.flattened_attached_emails), 2)
        attached_email0 = icon_email.flattened_attached_emails[0]
        attached_email1 = icon_email.flattened_attached_emails[1]

        self.assertEqual(attached_email0.subject, "Level 2 subject")
        self.assertEqual(attached_email1.subject, "Pic attached")

        attached_file0 = icon_email.flattened_attached_files[0]
        self.assertEqual(attached_file0.name, "example.com")

    def test_flatten_real_data(self):
        email_with_nested_attachments_text = read_file_to_string(
            f"{CURRENT_DIR}/payloads/2 level deep email attached.eml"
        )
        email_parser = EmailParser(self.logger)
        icon_email = email_parser.make_email_from_raw(
            message_from_string(email_with_nested_attachments_text),
            "fake_account",
        )

        icon_email.flatten()
        self.assertEqual(icon_email.subject, "Fw: 2 level deep email attached")
        self.assertEqual(len(icon_email.flattened_attached_emails), 2)
        self.assertEqual(len(icon_email.flattened_attached_files), 0)

        attached_email0 = icon_email.flattened_attached_emails[0]
        attached_email1 = icon_email.flattened_attached_emails[1]

        self.assertEqual(attached_email0.subject, "Attachment")
        self.assertEqual(attached_email1.subject, "Test Message Attachment Subject")

    def test_json_handler(self):
        icon_email = IconEmail()
        actual = icon_email.json_handler(b"some_bytes")
        self.assertEqual(actual, "c29tZV9ieXRlcw==")

        actual = icon_email.json_handler(IconFile())
        self.assertEqual(
            actual,
            {
                "name": "",
                "content": "",
                "content_type": "",
                "indicators": {
                    "md5": "d41d8cd98f00b204e9800998ecf8427e",
                    "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                },
            },
        )

        bad_test_object = dict(int_list=[1, 2, 3])

        with self.assertRaises(EmailParserException):
            icon_email.json_handler(bad_test_object)

        class GarbageObject:
            def __init__(self, object):
                self.data = object

        object_with_datetime = GarbageObject(datetime.datetime.now())

        actual = icon_email.json_handler(object_with_datetime)
        self.assertIsNotNone(
            actual
        )  # It's very difficult to test an actual value with time

    def test_hash(self):
        email_with_nested_attachments_text = read_file_to_string(
            f"{CURRENT_DIR}/payloads/hash_crash.eml"
        )
        email_parser = EmailParser(self.logger)
        icon_email = email_parser.make_email_from_raw(
            message_from_string(email_with_nested_attachments_text),
            "fake_account",
        )

        actual = icon_email.__hash__()

        print(type(actual))
        self.assertIsInstance(actual, int)
