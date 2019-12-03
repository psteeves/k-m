def decode_string(string, encoding_schema="utf-8-sig"):
    return string.decode(encoding_schema)


def replace_unicode_quotations(string, replacement="'"):
    string = string.replace("\u2018", replacement)  # left single
    string = string.replace("\u2019", replacement)  # right single
    string = string.replace("\u201c", replacement)  # left double
    string = string.replace("\u201d", replacement)  # right double
    return string


def strip_whitespace(string):
    string = string.replace("\r\n", "\n")
    string = string.replace("* ", "")
    string = string.strip()
    return string
