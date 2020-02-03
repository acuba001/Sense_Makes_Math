from flask import current_app
from app import cache
from . import sdk
from app.libraries import myResponse

timeout = 60 * current_app.config['PRINTFUL_DATA_FETCH_PER_DAY'] / 24


@cache.cached(timeout=timeout, key_prefix='getStockPrintfulCatalog')
def getStockPrintfulCatalog(WithVariants=True):
    """

    """
    controller = sdk.Printful()
    res = myResponse("printful")
    # context = inspect.stack()[0]

    errors = []
    products = []
    products_with_variants = []

    try:
        products.extend(controller.get("products"))

        if WithVariants:
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
