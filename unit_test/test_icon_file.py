from eml_parser.icon_file import IconFile
from unittest import TestCase


# This class tests icon file
class TestIconFile(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_file(self):
        icon_file = IconFile(
            file_name="test.txt", content="content", content_type="plain/text"
        )
        self.assertEqual(icon_file.name, "test.txt")
        self.assertEqual(icon_file.content, "content")
        self.assertEqual(icon_file.content_type, "plain/text")

    def test_make_serializable(self):
        icon_file = IconFile(
            file_name="test.txt", content="content", content_type="plain/text"
        )
        actual = icon_file.make_serializable()

        expected = {
            "content": "content",
            "content_type": "plain/text",
            "name": "test.txt",
        }
        self.assertEqual(actual, expected)
