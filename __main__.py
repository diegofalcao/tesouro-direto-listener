#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import logging
import time

from Crawler import Crawler
from SendEmail import SendEmail

INTERVAL_IN_MINUTES = 5

DEFAULT_THRESHOLD_VALUE = 13

logger = logging.getLogger()
logger.setLevel(logging.WARNING)


def usage():
    print 'This program checks the Tesouro Direto Market in intervals ' \
          'of %d minute(s) in order to identify if the tax of a selected ' \
          'product is above the threshold specified by the user.' \
          % INTERVAL_IN_MINUTES
    print ''
    print 'Usage: %s -i <tes_direto_prod_indices> -l <limiar>' % sys.argv[0]
    print '\nOptions:'
    print '\t-h : prints the help'
    print '\t-o : prints all the available tesouro direto product indices'


def beep():
    for i in range(0, 4):
        print "\a",  # plays a beep in an OS independent way

        time.sleep(0.5)


def trigger_action(item_name, threshold, tax):

    msg = 'A taxa do produto escolhido (' + item_name + ') ' \
          'encontra-se atualmente acima do limiar configurado!\n' \
          'Limiar configurado: ' + str(threshold) + '%\nValor atual: ' + tax

    print msg

    beep()


def sendEmail(msg):
    email_sender = SendEmail('smtp.gmail.com', 587, '<user>',
                             '<pass>')

    try:
        email_sender.send('<user>', 'TESOURO DIRETO THRESHOLD ',
                          msg)

    except EnvironmentError as err:
        logger.error(err)

        print 'There is a problem with your e-mail configuration. So, the ' \
              'program will not be able to notify you. Please, stop the ' \
              'program and fix the configuration!'


def verify_if_tax_is_above_threshold(THRESHOLD, item):
    actual_tax_str = item[2]

    actual_tax = float(actual_tax_str.strip('%').replace(',', '.'))

    if actual_tax >= float(THRESHOLD):
        logging.info('The threshold is above the tax, triggering action...')

        trigger_action(item[0], THRESHOLD, actual_tax_str)


def main(argv):

    logging.basicConfig()
    logger = logging.getLogger()

    idxItem = -1
    limiar = '0'

    crawler = Crawler()

    try:
        opts, args = getopt.getopt(argv, 'hoi:l:', ['help', 'options',
                                                    'idxItem=', 'limiar='])
        if not opts:
            usage()
            sys.exit(2)

    except getopt.GetoptError, err:
        print str(err)

        usage()

        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()

            sys.exit()
        elif opt == '-o':
            try:
                crawler.show_items_indexes()
            except IOError as err:
                print 'O mercado do Tesouro Direto está fechado no momento.' \
                      'Logo, não é possível realizar essa operação agora. ' \
                      'Tente novamente em breve.'

            sys.exit(2)

        elif opt in ("-i", "--idxItem"):
            idxItem = int(arg)
        elif opt in ("-l", "--limiar"):
            limiar = arg

    THRESHOLD = 0

    if limiar == '0':
        THRESHOLD = DEFAULT_THRESHOLD_VALUE
    else:
        THRESHOLD = limiar

    print '\n\nHit the CTRL+C to exit...\n'

    print 'You will be notified when the tax is equal ' \
          'or above %s%%...' % THRESHOLD
    print 'Listening to the following product: '

    lastProductValue = -1

    try:
        while True:

            try:
                items = crawler.getItems()

                #  Checking if the value has changed to print the new values...
                if lastProductValue != items[idxItem][2]:
                    print '%s' % items[idxItem][0],
                    print '%s' % items[idxItem][1],
                    print '%s' % items[idxItem][2]

                verify_if_tax_is_above_threshold(THRESHOLD, items[idxItem])

                lastProductValue = items[idxItem][2]

            except IOError as err:
                logger.warn(err)
                lastProductValue = -1

            time.sleep(60 * INTERVAL_IN_MINUTES)

    except KeyboardInterrupt:
        logger.debug('User pressed CTRL+C')

        sys.exit(0)

if __name__ == '__main__':
    status = main(sys.argv[1:])
    sys.exit(status)
