from flask_restful import Resource
import requests
import inspect

from app import app, cache
from app.errors.error_types import BadUrlError, ExternalServerError, InternalServerError
from app.libraries import myResponse

timeout = 60*app.config['PRINTFUL_DATA_FETCH_PER_DAY']/24

# Please See: https://www.printful.com/docs/

class PrintfulController(Resource):
    def __init__(self):
        self.base_url = 'https://api.printful.com/{}'
        
        self.valid_printful_resources = [
            'products',
            'store/products',
            'orders',
            'files',
            'shipping/rates',
            'countries',
            'tax/countries',
            'tax/rates'
            ]

    def isValidResource(self, name):
        return name in self.valid_printful_resources

    def get(self, ResourceName):
        res = myResponse("printful")
        context = inspect.stack()[0]

        if self.isValidResource(ResourceName):
            # Create url
            url = self.base_url.format(str(ResourceName))
        else:
            raise BadUrlError(url, None, context)

        # Load params
        params = {'Authorization': app.config['PRINTFUL_API_KEY']}

        # Make call to 'Printful' api
        xRes = requests.get(url, params=params).json()

        if xRes["code"] in [200]:
            # Return formated response
            return xRes["results"]
        else:
            raise ExternalServerError("printful", url, None, context)

    def post(self, Resource):
        pass

@cache.cached(timeout=timeout, key_prefix='getStockPrintfulCatalog')
def getStockPrintfulCatalog(WithVariants=True):
    controller = PrintfulController()
    res = myResponse("printful")
    context = inspect.stack()[0]
    errors = []
    products = []
    products_with_variants = []

    try:
        products.extend(controller.get("products"))
        if type(WithVariants) is "<class 'bool'>" and WithVariants:
            for product in products:
                product_api_url = "products/{}".format(product['id'])
                product_with_variants = controller.get(product_api_url)
                products_with_variants.append(product_with_variants)
    except BadUrlError as err:
        print(err.message)
        errors.append(err)
    except InternalServerError as err:
        errors.append(err)
    except ExternalServerError as err:
        errors.append(err)
    except BaseException as err:
        errors.append(err)

    if len(errors) > 0:
        return res.config({'code': 404, 'results': None, 'error': errors[0]})
    else:
        return res.config({'code': 200, 'results': products_with_variants, 'error': None})

#   VERSION 1.0.0
# from app.libraries import formatResponse, formatErrorMessage
# def isValidPrintfulEndpoint(name):
#     valid_printful_endpoints = [
#         'products',
#         'store/products',
#         'orders',
#         'files',
#         'shipping/rates',
#         'countries',
#         'tax/countries',
#         'tax/rates'
#         ]
#     isValid = name in valid_printful_endpoints
#     if not isValid:
#         raise 

# # Please See: https://www.printful.com/docs/


# def getPrintful(endpoint):
#     res = myResponse()

#     if isValidPrintfulEndpoint(endpoint):
#         context = inspect.stack()[0]
#         res.configureContext(context)
#         # Create url
#         url = 'https://api.printful.com/{}'.format(str(endpoint))

#     # Load params
#     params = {'Authorization': app.config['PRINTFUL_API_KEY']}

#     try:
#         # Make call to 'Printful' api
#         res = requests.get(url, params=params).json()

#         # Return formated response
#         return formatResponse(res, context)

#     except BadUrlError(url) as err:
#         return formatResponse(dict({'code': 404, 'result': None, 'error': err}), context)

# @cache.cached(timeout=timeout, key_prefix='getStockPrintfulCatalog')
# def getStockPrintfulCatalog():
#     products = getPrintful("products")['data']
#     return products

# @cache.cached(timeout=timeout, key_prefix='getStockPrintfulCatalogWithVariants')
# def getStockPrintfulCatalogWithVariants():
# 	context = inspect.stack()[0]
# 	products = getPrintful("products")['data']
# 	products_with_variants = []

# 	try:
# 		for product in products:
# 			product_api_url = "products/{}".format(product['id'])
# 			product_with_variants = getPrintful(product_api_url)['data']
# 			products_with_variants.append(product_with_variants)
# 	except Exception as err:
# 		err_message = formatErrorMessage(err, context)
#         return formatResponse(dict({'code': 404, 'result': None, 'error': err_message}), context)

# 	return products_with_variants