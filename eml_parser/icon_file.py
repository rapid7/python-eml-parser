import json

import eml_parser.helper as helper
from eml_parser.indicators import Indicators


class IconFile(object):
    def __init__(self, file_name: str = "", content_type: str = "", content: str = ""):
        self.name = file_name
        self.content = content
        self.content_type = content_type
        self.indicators = Indicators(content)

    # May not need this
    def make_serializable(self) -> dict:
        """Converts the File to a JSON-serializable, cleaned dict"""
        message_json = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
        message_json = json.loads(message_json, strict=False)

        message_json_clean = helper.clean(message_json)
        return message_json_clean

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.content == other.content
            and self.content_type == other.content_type
        )

    def __hash__(self):
        return hash(
            (
                "file_name",
                self.name,
                "content",
                self.content,
                "content_type",
                self.content_type,
            )
        )

    def __lt__(self, other):
        """ Less than, allows class to be sorted"""
        return self.name < other.name
