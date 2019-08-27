from app import app, cache

import requests
import inspect

timeout = 60*app.config['PRINTFUL_DATA_FETCH_PER_DAY']/24


# Please See: https://www.printful.com/docs/
def formatErrorMessage(error, context):
    ln = context.lineno
    fn = context.filename
    fnc = context.function
    template = "[LN {}] An error occured while executing {}.{}. Error thrown: {}"
    err_message = template.format(ln, fn, fnc, error)
    return err_message if error != None else str(error)

def formatResponse(response):
    code = response["code"]
    data =  [] if code != 200 else response["result"]
    error = formatErrorMessage(response['result'], inspect.stack()[0]) if code != 200 else None
    return {
        'code': code, 
        'data': data, 
        'error': error
        }

def getPrintful(endpoint):

    # Create url
    url = 'https://api.printful.com/{}'.format(str(endpoint) or "products")

    # Load params
    params = { 'Authorization': app.config['PRINTFUL_API_KEY'] }

    try:
        # Make call to 'Printful' api
        res = requests.get(url, params=params).json()

        # Return formated response
        return formatResponse(res)

    except Exception as err:
        print(formatErrorMessage(err, inspect.stack()[0]))

@cache.cached(timeout=timeout, key_prefix='getStockPrintfulCatalog')
def getStockPrintfulCatalog():
    products = getPrintful("products")['data']
    products_and_variants =  []
    for product in products:
        products_and_variants.append(getPrintful("products/{}".format(product['id']))['data'])
    return products_and_variants

