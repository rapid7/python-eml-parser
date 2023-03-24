
# InsightConnect Integrations Email Parser

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Markdown Lint](https://github.com/rapid7/python-eml-parser/workflows/Markdown%20Lint/badge.svg)
![Unit testing](https://github.com/rapid7/python-eml-parser/workflows/Unit%20testing/badge.svg)

Tooling for parse emails in [Rapid7 InsightConnect](https://www.rapid7.com/products/insightconnect/) plugins.

## Installation

```
pip install python-eml-parser
```

## Use

Simple!

### Python

```
from python-eml-parser.email_parser import EmailParser
from email import message_from_string


email_parser = EmailParser()
email = email_parser.make_email_from_raw(
    self.log, message_from_string(raw_email), mailbox_id
)
```

## Contributions

Contributions are welcome! This project utilizes [black](https://github.com/psf/black)
and [pre-commit](https://pre-commit.com/) for handling code
style. Simply follow the instructions for installing pre-commit and 
run `pre-commit install` in the repository after cloning and you will
be on your way to contributing!

## Changelog

* 2.0.0 - MD5, SHA1, and SHA256 Indicators for Base64 Content are now hashes of the decoded Base64 Content
* 1.0.0 - Initial release
