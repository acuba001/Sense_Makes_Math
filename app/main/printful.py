import requests
import inspect

from app import app, cache
from app.libraries import formatResponse, formatErrorMessage
from app.libraries import myResponse

timeout = 60*app.config['PRINTFUL_DATA_FETCH_PER_DAY']/24


def isValidPrintfulEndpoint(name):
    valid_printful_endpoints = [
        'products',
        'store/products',
        'orders',
        'files',
        'shipping/rates',
        'countries',
        'tax/countries',
        'tax/rates'
        ]
    isValid = name in valid_printful_endpoints
    if not isValid:
        raise 

# Please See: https://www.printful.com/docs/


def getPrintful(endpoint):
    res = myResponse()

    if isValidPrintfulEndpoint(endpoint):
        context = inspect.stack()[0]
        res.configureContext(context)
        # Create url
        url = 'https://api.printful.com/{}'.format(str(endpoint))

    # Load params
    params = {'Authorization': app.config['PRINTFUL_API_KEY']}

    try:
        # Make call to 'Printful' api
        res = requests.get(url, params=params).json()

        # Return formated response
        return formatResponse(res, context)

    except BadUrlError(url) as err:
        return formatResponse(dict({'code': 404, 'result': None, 'error': err}), context)

@cache.cached(timeout=timeout, key_prefix='getStockPrintfulCatalog')
def getStockPrintfulCatalog():
    products = getPrintful("products")['data']
    return products

@cache.cached(timeout=timeout, key_prefix='getStockPrintfulCatalogWithVariants')
def getStockPrintfulCatalogWithVariants():
	context = inspect.stack()[0]
	products = getPrintful("products")['data']
	products_with_variants = []

	try:
		for product in products:
			product_api_url = "products/{}".format(product['id'])
			product_with_variants = getPrintful(product_api_url)['data']
			products_with_variants.append(product_with_variants)
	except Exception as err:
		err_message = formatErrorMessage(err, context)
        return formatResponse(dict({'code': 404, 'result': None, 'error': err_message}), context)

	return products_with_variants

