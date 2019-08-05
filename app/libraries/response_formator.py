from bs4 import BeautifulSoup as soup
import re

def strip_html(raw_html):
    re.purge()
    
    # Strip HTML Tags
    template1 = re.compile(r"<.*?>")
    clean_html = re.sub(template1, '', raw_html)

    template2 = re.compile(r"/&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});/ig") 
    clean_html = re.sub(template2, '', clean_html)

    clean_html = clean_html.replace('\n', ' ')

    clean_html = clean_html.replace('&nbsp;', '')

    return clean_html # or soup(raw_html, 'html.parser').text
