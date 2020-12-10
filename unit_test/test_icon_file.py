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
        self.assertEqual(icon_file.indicators.md5, "9a0364b9e99bb480dd25e1f0284c8555")
        self.assertEqual(
            icon_file.indicators.sha1, "040f06fd774092478d450774f5ba30c5da78acc8"
        )
        self.assertEqual(
            icon_file.indicators.sha256,
            "ed7002b439e9ac845f22357d822bac1444730fbdb6016d3ec9432297b9ec9f73",
        )

    def test_make_serializable(self):
        icon_file = IconFile(
            file_name="test.txt", content="content", content_type="plain/text"
        )
        actual = icon_file.make_serializable()

        expected = {
            "content": "content",
            "content_type": "plain/text",
            "name": "test.txt",
            "indicators": {
                "md5": "9a0364b9e99bb480dd25e1f0284c8555",
                "sha1": "040f06fd774092478d450774f5ba30c5da78acc8",
                "sha256": "ed7002b439e9ac845f22357d822bac1444730fbdb6016d3ec9432297b9ec9f73",
            },
        }
        self.assertEqual(actual, expected)
