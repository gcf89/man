#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Module description
"""


import argparse
import logging
import logging.config
import subprocess
import re
from datetime import datetime
import locale



# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

def init_logger():
    """
    Initialize logger
    """

    loggin_config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s][%(levelname)9s]: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': 'out1.log',
                # 'mode': 'w',
                # 'encoding': 'utf-8',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
    }

    logging.config.dictConfig(loggin_config)


def test():
    """
    Simple docsting test
    """
    import doctest
    doctest.testmod()


def main():
    """
    Start point
    """

    # timeData=u'[ 24-янв-17 07:24 ]'    ### lower-case
    # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    # result = datetime.strptime(timeData.encode('utf-8'), u'[ %d-%b-%y  %H:%M ]')
    # print(result)

    

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--abs", dest="var_name", default="",
                        help="Default:")
    args = parser.parse_args()
    if args.var_name == 'value':
        pass

    # real input
    bash_cmd = "date"
    process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.strip() # ascii: для трансформации в unicode нужна следующая команда
    output = unicode(output, "utf-8") # чтобы сработало регулярное выражение: для re нужен префикс u обязательно и тут соотв. тоже

    # for testingpyli
    # output = 'Mon Jan 21 18:06:52 MSK 2018'
    # output = 'Wd nov 21 18:06:52 MSK 2018'
    # output = u'Пн ноя 21 18:06:52 MSK 2018'
    # output = u'Пн ноя 26'
    logging.debug(u'Output: {0}'.format(output))

    datetime_format_str = '%a %b %d %X %Z %Y'
    # datetime_format_str = '%a %b %d'
    # datetime_format_str = '%c'

    # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    # now = datetime.now()
    # now_str = now.strftime(datetime_format_str)
    # logging.debug('Now: {0}'.format(now_str))

    re_result = re.search(ur'[a-zA-Za-яА-ЯёЁ]{2}\s[a-zA-Za-яА-ЯёЁ]{3}\s\d{1,2}\s\d{1,2}\:\d{2}\:\d{2}\s\w{3}\s\d{4}', output)
    # re_result = re.search(ur'[a-zA-Za-яА-ЯёЁ]{2}\s[a-zA-Za-яА-ЯёЁ]{3}\s\d{1,2}', output)
    if re_result:
        logging.debug(u'Regexp parse result: {0}'.format(re_result.group(0)))
        try:
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
            result_date_time = datetime.strptime(output.encode('utf-8'), datetime_format_str)
            logging.debug(u'Datetime parsed successfully: {0}'.format(result_date_time))
        except ValueError as e:
            logging.error(u'Cannot parse input as datetime: {0}'.format(e))
    else:
        print 'Input is not a datetime!'


if __name__ == "__main__":
    # test()
    init_logger()
    logging.info('Started')
    main()
    logging.info('Finished')
