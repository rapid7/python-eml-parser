import re

_regex = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")


def get_emails_as_list(s: str) -> list:
    """Returns an iterator of matched emails found in string s."""
    list_of_emails = re.findall(_regex, s)
    return list_of_emails


def get_emails_as_string(s: str) -> str:
    """Returns an iterator of matched emails found in string s."""
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
    comma = ", "
    return comma.join(get_emails_as_list(s))
