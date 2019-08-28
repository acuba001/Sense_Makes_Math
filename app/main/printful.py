import requests
import inspect

from app import app, cache
from app.libraries import formatResponse, formatErrorMessage

timeout = 60*app.config['PRINTFUL_DATA_FETCH_PER_DAY']/24


# Please See: https://www.printful.com/docs/
@cache.cached(timeout=timeout, key_prefix='getPrintful')
def getPrintful(endpoint):

    # Create url
    url = 'https://api.printful.com/{}'.format(str(endpoint) or "products")

    # Load params
    params = { 'Authorization': app.config['PRINTFUL_API_KEY'] }

    try:
        # Make call to 'Printful' api
        res = requests.get(url, params=params).json()
        return formatResponse(res, inspect.stack()[0])

    except Exception as err:
        err_message = formatErrorMessage(err)
        print(err_message)
        return formatResponse({'code': 404, 'result': None, 'error': err_message})

@cache.cached(timeout=timeout, key_prefix='getStockPrintfulCatalogWithVariants')
def getStockPrintfulCatalogWithVariants():
    products = getPrintful("products")['data']
    
    products_with_variants =  []
    for product in products:
        product_with_variants = getPrintful("products/{}".format(product['id']))['data']
        products_with_variants.append(product_with_variants)
    return products_with_variants

