import re


def strip_html(raw_html):
    re.purge()

    # Strip HTML Tags
    template1 = re.compile(r"<.*?>")
    _html = re.sub(template1, '', raw_html)

    # Strip HTML extra characters
    template2 = re.compile(r"/&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});/ig")
    clean_html = re.sub(template2, '', _html)

    clean_html = clean_html.replace('\n', ' ')

    clean_html = clean_html.replace('&nbsp;', '')

    return clean_html
