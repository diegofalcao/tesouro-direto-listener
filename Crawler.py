#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import logging

from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.WARNING)

        self.URL = 'https://www.rico.com.vc/MinhaPagina/tesouro-direto/' \
                   'AllFixedIncomes.aspx'

    def __checkIfMarketIsClosed(self, soup):
        pageTitle = soup.find('title').text.strip()

        if pageTitle == 'Mercado Fechado':
            raise IOError('O mercado está fechado para operações. Portanto, '
                          'o monitoramento dos índices ficará inativo até que '
                          'o mercado volte a operar...')

    def getItems(self):
        data = []

        indexer = {}

        page = urllib2.urlopen(self.URL)

        soup = BeautifulSoup(page.read())

        self.__checkIfMarketIsClosed(soup)

        mainTable = soup.find('table', {'class': 'td-full-list-table'})

        index = 0

        for row in mainTable.findAll('tr')[1:]:
            cols = row.findAll('td')

            cols = [ele.text.strip() for ele in cols]

            # Get rid of empty values
            data.append([ele for ele in cols if ele])

            indexer[index] = data[index]

            index = index + 1

        if len(indexer) <= 1:
            raise IOError('Problems parsing the \'Tesouro Direto\' '
                          'page. This page is facing some problems '
                          'right now. So, be patient... they will fix it '
                          'soon.')

        return indexer

    def show_items_indexes(self):
        try:
            items = self.getItems()

            for index in items:
                print 'Índice %s para ' % index,
                print '%s' % items[index][0]

        except IOError as err:
            raise err
