import re
import os

"""
This is a quick utility to nuke emails, ips, and domains from test payload files.

To use this, simply drop your test in the payloads directory and run. It may produce
some weird results like example@example.example.com

That's OK. It shouldn't break the structure of the email you'd like to test. 
"""

_regex_email = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
_regex_domain = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}")
_regex_ip = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

def clean(contents):
    new_contents = re.sub(_regex_domain, "example.com", contents)
    new_contents = re.sub(_regex_email, "user@example.com", new_contents)
    new_contents = re.sub(_regex_ip, "198.162.1.1", new_contents)

    return new_contents

def main():
    cwd = os.getcwd()
    payloads_dir = cwd + "/payloads"
    filenames = os.listdir(payloads_dir)
    print(filenames)

    for file in filenames:
        cleaned_contents = ""
        current_file = f"{payloads_dir}/{file}"
        with open(current_file, 'r') as f:
            contents = f.read()
            cleaned_contents = clean(contents)

        with open(current_file, 'w') as f:
            f.write(cleaned_contents)

if __name__ == "__main__":
    main()
