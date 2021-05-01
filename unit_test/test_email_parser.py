from eml_parser.email_parser import EmailParser
from unittest import TestCase
import logging
import os
from email import message_from_string

TEST_MAILBOX_ID = "somedude@hotmail.com"

CURRENT_DIR = os.path.dirname(__file__)
GET_RAW_ATTACHMENT_PAYLOAD = f"{CURRENT_DIR}/payloads/four_deep_with_pic.txt"
GET_RAW_ATTACHMENT_PAYLOAD2 = f"{CURRENT_DIR}/payloads/get_raw_attachment_test.txt"
GET_RAW_ATTACHMENT_PAYLOAD3 = f"{CURRENT_DIR}/payloads/3_deep_with_text_attachment.txt"
GET_RAW_ATTACHMENT_PAYLOAD4 = f"{CURRENT_DIR}/payloads/basic_email_attachment.txt"
GET_DOUBLE_ATTACHED_WITH_IMAGES = (
    f"{CURRENT_DIR}/payloads/double_attached_with_images.txt"
)
GET_PAYLOAD_EVIL_EMAIL = f"{CURRENT_DIR}/payloads/evil_email.txt"
GET_BASIC_EMAIL = f"{CURRENT_DIR}/payloads/basic_email.txt"
GET_EML_WITH_EML_ATTACHED = f"{CURRENT_DIR}/payloads/lots_of_eml_attached.eml"
GET_ENCODED_EML = f"{CURRENT_DIR}/payloads/encoded_ms_eml.txt"
GET_UNICODE_EML = f"{CURRENT_DIR}/payloads/Grüße_von_Stefan_Appel.eml"
GET_GOOGLE_SURVEY = f"{CURRENT_DIR}/payloads/API Security Survey (please take this important survey) .eml"

GET_BAD_EMAIL1 = f"{CURRENT_DIR}/payloads/get_raw_attachment_test_no_content_type.txt"


# Get a real payload from file
def read_file_to_string(filename):
    with open(filename) as my_file:
        return my_file.read()


class TestEmailParser(TestCase):
    def setUp(self) -> None:
        self.log = logging.getLogger("stuff")

    def test_parse_from_raw(self):
        raw_email = read_file_to_string(GET_RAW_ATTACHMENT_PAYLOAD)
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        self.assertEqual(email.account, TEST_MAILBOX_ID)
        self.assertEqual(email.subject, "level 3")
        self.assertEqual(len(email.attached_emails), 2)
        self.assertEqual(len(email.attached_files), 1)

        self.assertEqual(email.date_received, "Thu, 8 Aug 2019 17:29:14 +0000")
        self.assertEqual(len(email.headers), 73)
        self.assertEqual(email.is_read, False)
        self.assertEqual(email.recipients, ["user@example.com"])
        self.assertEqual(email.sender, "user@example.com")
        self.assertTrue("level 3" in email.body)
        self.assertEqual(
            [d.md5 for d in email.indicators],
            ['b067a7ee9a159b724d5261dc80e03124', 'a35d0f590b9e2aa1a6afa68880836777', 'eae68e9c11349cc5dece3474acd87804', '224662a660009095b8eb905a9c0d6964', '68b329da9893e34099c7d8ad5cb9c940', '4ff3d0db8a6aa37b33bc70492b8d4c2c', '5288a1294c0c2d86ca05027996127aaa']
        )
        self.assertEqual(
            [d.sha1 for d in email.indicators],
            ['f62bfadaea976ecca214a0696188dfa409ba6478', '2b725fe68564fb791c5a33f451c3fbf589e1d2e8', 'b4f3aba8e4cd3a67f2bedd2166bf5e34a403f756', '8da1890238848f6b8f1c776b0699babb0925f256', 'adc83b19e793491b1c6ea0fd8b46cd9f32e592fc', '1f0dede6a71ddb34aefa595c618b380f7ed179ec', '32127d12c2133daa69663f684ff94773cb1fe0fd']
        )
        self.assertEqual(
            [d.sha256 for d in email.indicators],
            ['52b97144c63e5a585ba11550d3969e512d2394aca5252a1fbcea625964cdaae3', '226a485db0230d4bc95c892f29b7257fee1aefb9ed273ec4cc4abe134a6b8a6b', 'f05aeb4305d0f98daf964f851960d61daa3a2d73af2bc23140d047a312574ff9', '1950205c6953757c7edc8afa12cf26dc87d5e888a49828c997b404fe5fb51b3b', '01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b', 'e8c6adeb2cd035926a6ed70c8097264b56aa0c06cfa387fd9bd0a789b0fe0a00', '20b4681499193a3a5c647c7e6af71f2f2daf7ac9204d3a5d8c203cf84ce27782'],
        )

        attached_email = email.attached_emails[0]
        self.assertEqual(attached_email.subject, "Level 2 subject")
        self.assertEqual(attached_email.sender, "user@example.com")
        self.assertEqual(attached_email.recipients, ["user@example.com"])
        self.assertTrue("Level 2 body" in attached_email.body)
        self.assertEqual(
            [d.md5 for d in attached_email.indicators],
            ['eae68e9c11349cc5dece3474acd87804', '224662a660009095b8eb905a9c0d6964', '68b329da9893e34099c7d8ad5cb9c940', '4ff3d0db8a6aa37b33bc70492b8d4c2c', '5288a1294c0c2d86ca05027996127aaa']
        )
        self.assertEqual(
            [d.sha1 for d in attached_email.indicators],
            ['b4f3aba8e4cd3a67f2bedd2166bf5e34a403f756', '8da1890238848f6b8f1c776b0699babb0925f256', 'adc83b19e793491b1c6ea0fd8b46cd9f32e592fc', '1f0dede6a71ddb34aefa595c618b380f7ed179ec', '32127d12c2133daa69663f684ff94773cb1fe0fd']
        )
        self.assertEqual(
            [d.sha256 for d in attached_email.indicators],
            ['f05aeb4305d0f98daf964f851960d61daa3a2d73af2bc23140d047a312574ff9', '1950205c6953757c7edc8afa12cf26dc87d5e888a49828c997b404fe5fb51b3b', '01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b', 'e8c6adeb2cd035926a6ed70c8097264b56aa0c06cfa387fd9bd0a789b0fe0a00', '20b4681499193a3a5c647c7e6af71f2f2daf7ac9204d3a5d8c203cf84ce27782']
        )

        attached_email_of_attached_email = attached_email.attached_emails[0]
        self.assertEqual(attached_email_of_attached_email.subject, "Pic attached")

        attached_file = email.attached_files[0]
        self.assertEqual(attached_file.content[:5], "iVBOR")
        self.assertEqual(attached_file.content_type, "image/png")
        self.assertEqual(attached_file.name, "example.com")
        self.assertEqual(
            attached_file.indicators.md5, "539cefc749ed1d78e3c821307f7c1b0a"
        )
        self.assertEqual(
            attached_file.indicators.sha1, "9a95c01f15c461708733dac2b3fbe10901801582"
        )
        self.assertEqual(
            attached_file.indicators.sha256,
            "ac92883cdc6cda0735f9c3f968e6103f8dd93f705cc077dce70924eda523a916",
        )

    def test_parse_from_raw2(self):
        raw_email = read_file_to_string(GET_RAW_ATTACHMENT_PAYLOAD2)
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        self.assertEqual(email.account, TEST_MAILBOX_ID)
        self.assertEqual(email.subject, "Attachment")
        self.assertTrue("Attachment Body" in email.body)
        self.assertEqual(
            [d.md5 for d in email.indicators],
            ['efb42a638c23407056c48ebab5e119eb', '267cc9490cec0c3229795e5eb7ef2a25', '6f3a888cc847bb3fc76f55bf9a4c1781', 'd8fbc36661e49768c7db3160afdeaf70']
        )
        self.assertEqual(
            [d.sha1 for d in email.indicators],
            ['057858fe08a55ad2d1e4ee4a2d26a88a6a954691', 'e62d99edae16e70bfcf9bd041c08afd183271c56', '18ada0598635438ea49a305102b6d6e84e6afaa7', 'bfccda3b5ade42569e05753fa1ad1f05c4ce2095']
        )
        self.assertEqual(
            [d.sha256 for d in email.indicators],
            ['91557d129de7ce80a6ac78f6c17a9d5aec7ff4dc777f1f0e69d3b2f1568a5cb1', 'aae84980564cc107ea5ef7c3ea393fb18d678fea5956b7b5005f8ae7664bf78c', 'd5ef2912c4b28072c1f9df611f87b683c1b31cfb609f5d4f09be5abaf8c6bf18', 'b6ef02bc495b3710bd822a789e2b916c610b6fc78aab1f5a82bb2676fd6ad664']
        )
        self.assertEqual(len(email.attached_emails), 1)
        self.assertEqual(len(email.attached_files), 0)

        self.assertTrue("Attachment Body" in email.body)
        attached_email = email.attached_emails[0]
        self.assertTrue("Test Message Attachment Body" in attached_email.body)
        self.assertEqual(
            [d.md5 for d in attached_email.indicators],
            ['6f3a888cc847bb3fc76f55bf9a4c1781', 'd8fbc36661e49768c7db3160afdeaf70']
        )
        self.assertEqual(
            [d.sha1 for d in attached_email.indicators],
            ['18ada0598635438ea49a305102b6d6e84e6afaa7', 'bfccda3b5ade42569e05753fa1ad1f05c4ce2095']
        )
        self.assertEqual(
            [d.sha256 for d in attached_email.indicators],
            ['d5ef2912c4b28072c1f9df611f87b683c1b31cfb609f5d4f09be5abaf8c6bf18', 'b6ef02bc495b3710bd822a789e2b916c610b6fc78aab1f5a82bb2676fd6ad664']
        )

        self.assertEqual(email.date_received, "Tue, 6 Aug 2019 19:19:40 +0000")
        self.assertEqual(len(email.headers), 75)
        self.assertEqual(email.is_read, False)
        self.assertEqual(email.recipients, ["user@example.com"])
        self.assertEqual(email.sender, "user@example.com")

    def test_parse_from_raw3(self):
        raw_email = read_file_to_string(GET_RAW_ATTACHMENT_PAYLOAD3)
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        self.assertEqual(email.account, TEST_MAILBOX_ID)
        self.assertEqual(email.subject, "Text Attachment")
        self.assertEqual(len(email.attached_emails), 0)
        self.assertEqual(len(email.attached_files), 1)

        self.assertTrue("Here is a text attachment" in email.body)
        self.assertEqual(email.date_received, "Thu, 8 Aug 2019 20:16:38 +0000")
        self.assertEqual(len(email.headers), 76)
        self.assertEqual(email.is_read, False)
        self.assertEqual(email.recipients, ["user@example.com"])
        self.assertEqual(email.sender, "user@example.com")

        attachment = email.attached_files[0]
        self.assertEqual(attachment.content_type, "text/plain")
        expected_content = "VGhpcyBpcyBhIHRlc3QgYXR0YWNobWVudA0KDQpJdCBoYXMgc29tZSB0ZXh0IGluIGl0LiANCg0KYWFkcm9pZC5uZXQNCg=="
        self.assertEqual(attachment.content, expected_content)
        self.assertEqual(attachment.name, "test_example.com")
        self.assertEqual(attachment.indicators.md5, "593aa3b46e3902094303b7ef1349d9ff")
        self.assertEqual(
            attachment.indicators.sha1, "d1181c07e87d73803bf5786b37e8f03a176290a2"
        )
        self.assertEqual(
            attachment.indicators.sha256,
            "c08eb82e5383760cad3a4b4863dfb871b4c4252eba039c64a90ffc818907de27",
        )

    def test_parse_from_raw4(self):
        raw_email = read_file_to_string(GET_RAW_ATTACHMENT_PAYLOAD4)
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        self.assertEqual(email.account, TEST_MAILBOX_ID)
        self.assertEqual(email.subject, "Basic Message Attachment")
        self.assertEqual(len(email.attached_emails), 0)
        self.assertEqual(len(email.attached_files), 0)

        expected_body = """<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<style type="text/css" style="display:none;"> P {margin-top:0;margin-bottom:0;} </style>
</head>
<body dir="ltr">
<div style="font-family: Calibri, Helvetica, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);">
Nothing here, just this text</div>
</body>
</html>
"""
        self.assertEqual(email.body, expected_body)
        self.assertEqual(
            [d.md5 for d in email.indicators],
            ['99d3bb8f3b3d3e51dc40b749174f9f90', 'c537b7db873e8e2cd6b965be6afdd063']
        )
        self.assertEqual(
            [d.sha1 for d in email.indicators],
            ['9c9ac62540543d3b20722f1fabb31b3a363547b7', 'b1f5dd056c0930042fa5549b4c5c8aa6ecb70e3a']
        )
        self.assertEqual(
            [d.sha256 for d in email.indicators],
            ['9b3ba7c8a896fba147e01cc5ea7416707b668d674200b6b4d754248f96310438', '50b779af79f6493165c0b8de3e56c08e0cc3eec3c50e2f9f2ddfe80247b8e886']
        )
        self.assertEqual(email.date_received, "Thu, 8 Aug 2019 21:19:37 +0000")
        self.assertEqual(len(email.headers), 76)
        self.assertEqual(email.is_read, False)
        self.assertEqual(email.recipients, ["user@example.com"])
        self.assertEqual(email.sender, "user@example.com")

    def test_parse_from_raw_evil_email(self):
        raw_email = read_file_to_string(GET_PAYLOAD_EVIL_EMAIL)
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        self.assertEqual(email.account, TEST_MAILBOX_ID)
        self.assertEqual(email.subject, "FW: [POTENTIAL PHISH] MESINC")
        self.assertEqual(len(email.attached_emails), 2)
        self.assertEqual(len(email.attached_files), 4)

        self.assertEqual(email.date_received, "Thu, 1 Aug 2019 10:36:33 +0000")
        self.assertEqual(len(email.headers), 69)
        self.assertEqual(email.is_read, False)
        self.assertEqual(
            email.recipients,
            [
                "user@example.com",
                "user@example.com",
            ],
        )
        self.assertEqual(email.sender, "user@example.com")
        self.assertEqual(
            [d.md5 for d in email.indicators],
            ['91d6dc1ec546d719e4eaddb46cfc47c2', '1f224c7839c3f7d825864f322a6bb57a', '37f34918dfbed1979275686b65d572c9', '074480fdee5ca23a2dfde056f248eb8f', '907729a50f97b5da110eedc1555f77de', 'd6a82ae5b3ab8b85a2b2ea6bdff5c2fa', '7eebac1ee4a603f1e1e9cedae18e23b4', 'b2c83a9ce3b0e272f219376a91d643be', '9a160749c91a0f1fbd91edb6b6b43fa7', '885d96a24039dbdf336748df9fa08b48']
        )
        self.assertEqual(
            [d.sha1 for d in email.indicators],
            ['eff5fc65becb9a7ef1732b1432715ff0c8d78276', '83dfe966303673168c344c286bb16d2801d1919f', '51f435e29cae0fd70e196c5b2b11f4db66c40f43', 'cd8965f9fc5519776c014ed27b8d5f6d7c0b16d2', '0f6893f573a5ec144411a513c154b4cd3a988975', '849c94583692c1f5b76bd3285e07083a71963f94', '1ff7f7880f96a79e61d65cad0daf532145cd0ed7', '8c65f765413465dd8ba9d24c29d95370b6a4fccb', 'e7e143b11126941f6fe17b4f2873d4b8972d5b70', '19b0930b78551044f87fae9b31d27fc7499a605d']
        )
        self.assertEqual(
            [d.sha256 for d in email.indicators],
            ['4e7728bf05c87767efa7ca46f3ff5322d12899747905938cf1db85d966c878f3', '251ac384891e16088f0be97cf6a872559fd287f1e163e4b83f6b49b8ad6862b8', '972435f55a4c05660671788c6f9d057f8d206c623c5c100b29ce877899e9793d', 'c116993e5b12738cb974180caa01a34b89b9485790882778ca67fa0750b094d6', '661683f1bee1c0d4556ee5cd9b197cbb39c04da48adf9d8483717d1790863739', 'a600775a1b81fb63b2572f2c5b5b718a059da4412b28b0cd40cde2a07cb66806', '33d352f4ba43792e366e330cf9c8ac9fe9d8da55972504629742330449701a35', 'd3ccc5a5e58aebe7e2dddbfecda746accf08d2294572a791bee3b8c9404b73fe', '2956991d59472e5995189a3f7f5af52c0de9cefcfaf1824631f4c47239aa5f6a', 'a7cb0f9d5f5036d44eb2464458e3a264c0cac33c6f113f25b2eab451381bff2c']
        )

    def test_parse_google_link_garbled(self):
        raw_email = read_file_to_string(GET_GOOGLE_SURVEY)
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        self.assertTrue(
            '<a href="http://aexample.com/" rel="nofollow" target="_blank">'
            in email.body
        )

    def test_parse_raw_with_unicode(self):
        raw_email = read_file_to_string(GET_UNICODE_EML)
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        self.assertEqual(email.subject, "Grüße von Stefan Appel")

    def test_parse_double_attached_with_images(self):
        raw_email = read_file_to_string(GET_DOUBLE_ATTACHED_WITH_IMAGES)
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        self.assertEqual(email.account, TEST_MAILBOX_ID)
        self.assertEqual(email.subject, "Fw: User Test")
        self.assertEqual(len(email.attached_emails), 2)
        self.assertEqual(len(email.attached_files), 2)

        self.assertEqual(email.date_received, "Tue, 13 Aug 2019 20:05:12 +0000")
        self.assertEqual(len(email.headers), 53)
        self.assertEqual(email.is_read, False)
        self.assertEqual(email.recipients, ["user@example.com"])
        self.assertEqual(email.sender, "user@example.com")

        email1 = email.attached_emails[0]
        email2 = email.attached_emails[1]

        self.assertTrue(email1.subject, "Pic and eml attached")
        self.assertTrue(email2.subject, "Test Email")

        attached_file = email.attached_files[0]
        self.assertEqual(
            attached_file.indicators.md5, "2fca7949ad1004cefe685b81c3889e1c"
        )
        self.assertEqual(
            attached_file.indicators.sha1, "b7e20bc9d4eb40adb1c4f103821bd461deab9d3f"
        )
        self.assertEqual(
            attached_file.indicators.sha256,
            "8477aeb65fe7985cc82bc8f231ebfc519b8178d1050a9cee7f1b450e6c370240",
        )

    def test_single_recipient(self):
        email_parser = EmailParser(self.log)
        msg = {"To": "bob@hotmail.com"}
        rcpt = email_parser.get_recipients(msg)
        self.assertEqual(rcpt, ["bob@hotmail.com"])

    def test_no_recipients(self):
        email_parser = EmailParser(self.log)
        msg = {"To": ""}
        rcpt = email_parser.get_recipients(msg)
        self.assertEqual(rcpt, [])

    def test_multiple_recipients(self):
        email_parser = EmailParser(self.log)
        msg = {
            "To": "<someguy@microsoft.com> bob smith, <someotherguy@gmail.com> robert the bruce"
        }
        rcpt = email_parser.get_recipients(msg)
        self.assertEqual(rcpt, ["someguy@microsoft.com", "someotherguy@gmail.com"])

    def test_multiple_recipients_delivered_to(self):
        email_parser = EmailParser(self.log)
        msg = {
            "Delivered-To": "<someguy@microsoft.com> bob smith, <someotherguy@gmail.com> robert the bruce"
        }
        rcpt = email_parser.get_recipients(msg)
        self.assertEqual(rcpt, ["someguy@microsoft.com", "someotherguy@gmail.com"])

    def test_recipients_not_available(self):
        email_parser = EmailParser(self.log)
        msg = {}
        rcpt = email_parser.get_recipients(msg)
        self.assertEqual(rcpt, [])

    def test_decode_body(self):
        basic_email_text = read_file_to_string(GET_BASIC_EMAIL)
        test_email = message_from_string(basic_email_text)

        email_parser = EmailParser(self.log)
        actual_body = email_parser.decode_body(test_email)

        self.assertEqual(actual_body, "Test\n")

    def test_decode_body_unicode(self):
        basic_email_text = read_file_to_string(GET_BASIC_EMAIL)
        test_email = message_from_string(basic_email_text)
        test_email._payload = 'u"é'

        email_parser = EmailParser(self.log)
        actual_body = email_parser.decode_body(test_email)

        self.assertEqual(actual_body, 'u"')

    def test_decode_multipart_body_unicode(self):
        raw_text = read_file_to_string(GET_DOUBLE_ATTACHED_WITH_IMAGES)
        test_email = message_from_string(raw_text)

        email_parser = EmailParser(self.log)
        test_email._payload[0]._payload[0]._payload = (
            test_email._payload[0]
            ._payload[0]
            ._payload.replace("user@example.com", 'u"é')
        )
        actual_body = email_parser.decode_body(test_email._payload[0]._payload[0])

        expected_body = """________________________________From: Example User <u">Sent: Tuesday, August 13, 2019 3:56 PMTo: Example User <u">Subject: User Test________________________________From: Example User <u">Sent: Tuesday, August 13, 2019 10:55 AMTo: Example User <u">Subject: Fw: Short Test Email________________________________From: Example UserSent: Tuesday, August 13, 2019 9:30 AMTo: u" <u">Subject: Short Test Email"""
        self.assertEqual(expected_body, actual_body)

    def test_decode_multipart_body_html_unicode(self):
        raw_text = read_file_to_string(GET_DOUBLE_ATTACHED_WITH_IMAGES)
        test_email = message_from_string(raw_text)

        email_parser = EmailParser(self.log)
        test_email._payload[0]._payload[1]._payload = '<html>FOO u"é BAR</html>'
        actual_body = email_parser.decode_body(test_email._payload[0])

        expected_body = '<html>FOO u"é BAR</html>'
        self.assertEqual(expected_body, actual_body)

    def test_parse_attached_eml(self):
        raw_email = read_file_to_string(GET_EML_WITH_EML_ATTACHED)
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        self.assertEqual(len(email.attached_emails), 4)
        self.assertEqual(len(email.attached_files), 2)

    def test_decode_quoted_printable(self):
        raw_email = read_file_to_string(f"{CURRENT_DIR}/payloads/quoted_printable.eml")
        email_parser = EmailParser(self.log)
        email = email_parser.make_email_from_raw(
            message_from_string(raw_email), TEST_MAILBOX_ID
        )

        expected = '<p class="MsoNormal"><a href="http://example.com" title="http://proteexample.com.com/s/414KCXDXZofXVRNRZT6ai-n?domain=example.com">http://aexample.com</a><o:p></o:p></p>'
        self.assertTrue(expected in email.body)
