import hashlib
import json

import eml_parser.helper as helper


class Indicators(object):
    def __init__(self, content: str):
        encoded_content = content.encode("UTF-8")
        self.md5 = hashlib.md5(encoded_content).hexdigest()
        self.sha1 = hashlib.sha1(encoded_content).hexdigest()
        self.sha256 = hashlib.sha256(encoded_content).hexdigest()

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
            self.md5 == other.md5
            and self.sha1 == other.sha1
            and self.sha256 == other.sha256
        )

    def __hash__(self):
        return hash(
            (
                "md5",
                self.md5,
                "sha1",
                self.sha1,
                "sha256",
                self.sha256,
            )
        )
