from flask_restful import Resource
import requests
import inspect

from app import app, cache
from app.errors import BadUrlError, InternalServerError
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

    def isValid(self, endpoint):

        valid_printful_resources = [
            'products',
            'store/products',
            'orders',
            'files',
            'shipping/rates',
            'countries',
            'tax/countries',
            'tax/rates'
        ]
        return endpoint in valid_printful_resources

    def get(self, endpoint):
        context = inspect.stack()[0]

        # Create url
        #
        # [WIP] This current only works with base endpoints.
        # We need to expand the 'isValid' function to deal with
        # other cases
        #
        # if self.isValid(endpoint):
        url = self.base_url.format(str(endpoint))
        # else:
        #     raise BadUrlError(url, None, context)

        # Load params
        params = {
            'Authorization': app.config['PRINTFUL_API_KEY']
        }

        # Make call to 'Printful' api
        xRes = requests.get(url, params=params).json()

        if xRes["code"] in [200]:
            # Return formated response
            return xRes["result"]
        else:
            raise InternalServerError(None, context, "printful", url)

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
    except Exception as err:
        errors.append(err)

    print(str(errors))

    if len(errors) > 0:
        return res.config({'code': 404, 'results': None, 'error': errors[0]})
    else:
        payload = products_with_variants if WithVariants else products
        return res.config({'code': 200, 'results': payload, 'error': None})
# =============================================================================================================================================
# Printful API
#
#
#   SUB                   METHOD        URL                                         PARAMS                      RESPONSE
# =============================================================================================================================================
# Catalog               | GET       | ~/products                                  | NONE            |   { code: 200, result: Product[] }
#                       | GET       | ~/products/variant/{ varId }                | varId           |   { code: 200, result: { var: Variant, prod: Product }}
#                       | GET       | ~/products/{ prodId }                       | prodId          |   { code: 200, result: { prod: Product, var: Variant[] }}
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Products              | GET       | ~/store/products                            | status,         |   { code: 200, result: SyncProduct[], paging: Paging }
#                       |           |                                             | offset,         |
#                       |           |                                             | limit           |
#                       | POST      | ~/store/products                            | sync_product,   |   { code: 200, result: RequestProductResponse }
#                       |           |                                             | sync_variants   |
#                       | GET       | ~/store/products/{ sync_prodId }            | sync_prodId     |   { code: 200, result: { prod: SyncProduct, var: SyncVariant[] }}
#                       | DELETE    | ~/store/products/{ sync_prodId }            | sync_prodId     |   { code: 200, result: { prod: Product, var: Variant[] }}
#                       | PUT       | ~/store/products/{ sync_prodId }            | sync_product    |   { code: 200, result: RequestProductResponse }
#                       |           |                                             | sync_variants   |
#                       | POST      | ~/store/products/{ sync_prodId }/variants   | sync_prodId     |   { code: 200, result: RequestVariantResponse }
#                       | GET       | ~/store/variants/{ sync_varId }             | sync_varId      |   { code: 200, result: { prod: SyncVariant, var: SyncProduct }}
#                       | DELETE    | ~/store/variants/{ sync_varId }             | sync_varId      |   { code: 200, result: { prod: SyncVariant, var: SyncProduct }}
#                       | PUT       | ~/store/variants/{ sync_varId }             | sync_varId      |   { code: 200, result: RequestVariantResponse }
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Orders                | GET       | ~/orders                                    | status,         |   { code: 200, result: Order[], paging: Paging }
#                       |           |                                             | offset,         |
#                       |           |                                             | limit           |
#                       | POST      | ~/orders                                    | OrderInput,     |   { code: 200, result: Order }
#                       |           |                                             | confirm,        |
#                       |           |                                             | update_existing,|
#                       | POST      | ~/orders/estimate-costs                     | OrderInput      |   { code: 200, result: OrderCosts }
#                       | GET       | ~/orders/{ orderId }                        | orderId         |   { code: 200, result: Order}
#                       | DELETE    | ~/orders/{ orderId }                        | orderId         |   { code: 200, result: Order}
#                       | PUT       | ~/orders/{ orderId }                        | orderId,        |   { code: 200, result: Order}
#                       |           |                                             | confirm,        |
#                       |           |                                             | OrderInput      |
#                       | POST      | ~/orders/{ orderId }/confirm                | orderId         |   { code: 200, result: Order}
# --------------------------------------------------------------------------------------------------------------------------------------------
# File Library          | GET       | ~/files                                     | status,         |   { code: 200, result: File[], paging: Paging }
#                       |           |                                             | offset,         |
#                       |           |                                             | limit           |
#                       | POST      | ~/files                                     | File            |   { code: 200, result: File }
#                       | GET       | ~/files/{ fileId }                          | fileId          |   { code: 200, result: File }
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Shipping Rate         | POST      | ~/shipping/rates                            | AddressInfo,    |   { code: 200, result: ShippingInfo[] }
#                       |           |                                             | ItemInfo[],     |
#                       |           |                                             | currency        |
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Country/State Code    | GET       | ~/countries                                 | None            |   { code: 200, result: Country[] }
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Tax Rate              | GET       | ~/tax/countries                             | None            |   { code: 200, result: Country[] }
#                       | POST      | ~/tax/rates                                 | TaxRequest      |   { code: 200, result: TaxInfo }
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Webhook               |||
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Store Information     |||
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Mockup Generator      |||
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Warehouse Products    |||
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Warehouse Shipments   |||
# ---------------------------------------------------------------------------------------------------------------------------------------------
# E-comm Platform Sync  |||
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Webhook Simulator     |||
# --------