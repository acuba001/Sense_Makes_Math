from flask_restful import Resource
import requests
import inspect

from app import app, cache
from app.errors.error_types import BadUrlError, ExternalServerError, InternalServerError
from app.libraries import myResponse

timeout = 60*app.config['PRINTFUL_DATA_FETCH_PER_DAY']/24

# 

class PrintfulController(Resource):
    """
    Please See: https://www.printful.com/docs/ for 
    further details ont he Printful Api
    """
    def __init__(self):
        self.base_url = 'https://api.printful.com/{}'

    def get(self, endpoint):
            
        context = inspect.stack()[0]
        
        def isValid(self, endpoint):
            
            valid_printful_resources = [
                'products' ,
                'store/products',
                'orders',
                'files',
                'shipping/rates',
                'countries',
                'tax/countries',
                'tax/rates'
                ]
            return endpoint in valid_printful_resources
        
        # [WIP] This current only works with base endpoints. 
        # We need to expand the 'isValid' function to deal with
        # other cases
        # 
        # if self.isValid(endpoint):
        #     url = self.base_url.format(str(endpoint))
        # else:
        #     raise BadUrlError(url, None, context)

        # Create url
        url = self.base_url.format(str(endpoint))

        # Load params
        params = {'Authorization': app.config['PRINTFUL_API_KEY']}

        # Make call to 'Printful' api
        xRes = requests.get(url, params=params).json()

        if xRes["code"] in [200]:
            # Return formated response
            return xRes["result"]
        else:
            raise ExternalServerError("printful", url, None, context)

    def post(self, Resource):
        pass

@cache.cached(timeout=timeout, key_prefix='getStockPrintfulCatalog')
def getStockPrintfulCatalog(WithVariants=True):
    """
    
    """
    controller = PrintfulController()
    res = myResponse("printful")
    context = inspect.stack()[0]
    errors = []
    products = []
    products_with_variants = []

    try:
        products.extend(controller.get("products"))

        if type(WithVariants) is type(True) and WithVariants:
            for product in products:
                product_api_url = "products/{}".format(product['id'])
                product_with_variants = controller.get(product_api_url)
                products_with_variants.append(product_with_variants)
    except BadUrlError as err:
        print(str(err))
        errors.append(err)
    except InternalServerError as err:
        print(str(err))
        errors.append(err)
    except ExternalServerError as err:
        print(str(err))
        errors.append(err)
    except Exception as err:
        print(str(err))
        errors.append(err)

    if len(errors) > 0:
        return res.config({'code': 404, 'results': None, 'error': errors[0]})
    else:
        payload = products_with_variants if WithVariants else products
        return res.config({'code': 200, 'results': payload, 'error': None})
