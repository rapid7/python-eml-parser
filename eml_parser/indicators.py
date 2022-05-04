import hashlib
import json

import eml_parser.helper as helper
from eml_parser.constants import HEADERS, INDICATORS


class Indicators(object):
    def __init__(self, content: str, headers: list):
        encoded_content = content.encode("UTF-8")
        self.md5 = hashlib.md5(encoded_content).hexdigest()
        self.sha1 = hashlib.sha1(encoded_content).hexdigest()
        self.sha256 = hashlib.sha256(encoded_content).hexdigest()

        auth_types = self.parse_auth_results_header(headers)
        self.dkim = auth_types.get(INDICATORS.get("dkim"), None)
        self.dmarc = auth_types.get(INDICATORS.get("dmarc"), None)
        self.spf = auth_types.get(INDICATORS.get("spf"), None)

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

    @staticmethod
    def parse_auth_results_header(headers: list) -> dict:
        value = ""
        auth_types = {}

        if headers:
            for header in headers:
                name = header.get("name")
                if name == HEADERS.get("authentication_results"):
                    value = header.get("value")
                    break

        if value:
            split_header = value.split(";")
            for auth_type in split_header:
                stripped_auth_type = auth_type.strip().replace("\n", "")
                if stripped_auth_type.startswith("dkim"):
                    auth_types[INDICATORS.get("dkim")] = stripped_auth_type
                elif stripped_auth_type.startswith("dmarc"):
                    auth_types[INDICATORS.get("dmarc")] = stripped_auth_type
                elif stripped_auth_type.startswith("spf"):
                    auth_types[INDICATORS.get("spf")] = stripped_auth_type

        return auth_types
