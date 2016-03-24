#!/usr/bin/env python
import re
import urllib
import requests
from flask import Flask, url_for, request, jsonify
from scrapy.selector import Selector

app = Flask(__name__)

product = dict()
session = requests.session()

@app.route('/u/<path:url>', methods=['GET', 'POST'])
def get_item(url):
    global product

    product_id = request.args.get('id')

    if product_id != None:

        product['product_url'] = url+"?id="+product_id
        product['product_id'] = product_id

        productpage = (session.get(product['product_url'])).text
        prod_name =  Selector(text=productpage).xpath("//h3[@class='tb-main-title']/text()").extract()
        product['product_name'] = re.sub('\s+', '', prod_name[-1])
        prod_promo_price = Selector(text=productpage).xpath("//em[@class='tb-rmb-num']/text()").extract()
        product["product_price_range"] = prod_promo_price[0]
        prod_main_image = Selector(text=productpage).xpath("//img[@id='J_ImgBooth']/@src").extract()
        product["product_main_image"] = prod_main_image[0]

    elif re.match("[https?://]*world\.taobao\.com/item/[0-9]+", url) is not None:
        print "2nd"
    else:
    	print "_"
    return jsonify(product)

if __name__ == '__main__':
    app.run()
