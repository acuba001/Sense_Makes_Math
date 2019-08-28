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

    return clean_html

def formatErrorMessage(error, context):
    err_message = None
    ln = str(context.lineno or None)
    fn = str(context.filename.rpartition("/")[2].rpartition(".")[0] or None)
    fnc = str(context.function or None)
    template = "[LN {}] An error occured while executing {}.{}. Error thrown: {}" if context else "Sorry, something went wrong! Please trya gain later. Error Thrown: {}"
    err_message = template.format(ln, fn, fnc, error) if context else template.format(error)

    return err_message if error != None else str(error)


def formatResponse(response, context):
    code = response["code"]
    data = [] if not code in [200] else response["result"]
    error = formatErrorMessage(response['result'], context) if not code in [200] else str(None)
    return {
        'code': code,
        'data': data,
        'error': error
    }
