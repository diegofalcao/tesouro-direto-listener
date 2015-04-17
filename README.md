# tesouro-direto-listener

Description
=============

This program checks the Tesouro Direto Market in intervals of 5 minutes in order to identify if the tax of a selected product is above the threshold specified by the user.

How to execute
=============

This programs depends on BeautifulSoup module in order to crawl the webpage containing the Tesouro Direto Taxes. For more information, visit the project site.

In order to install this module, run the following command:

$ pip install beautifulsoup4
$ python __main__.py -i <tesouro_direto_prod_index> < -l <threshold>

You can check all the product indexes with the following command:
$ python __main__.py -o
