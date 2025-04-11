#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert CVS to Markdown (pretty import cvs table to redmine wiki)
"""


import argparse
import logging
import logging.config
import csv
from prettytable import PrettyTable


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
                'level':'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            'file':{
                'level':'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': 'cvs_to_markdown_table.log',
                # 'mode': 'w',
                'encoding': 'utf-8',
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

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input_csv",
                        help="Input file in CSV format",
                        required=True)
    parser.add_argument("-o", "--output", dest="output_md",
                        help="Output in MD format (good for Redmine wiki)",
                        required=True)
    args = parser.parse_args()

    result = PrettyTable()
    with open(args.input_csv, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        cols = 0
        for row in spamreader:
            if cols == 0:
                cols = len(row)
                headers = []
                for col in row:
                    headers.append(col)

                result.field_names = headers
                continue

            # print ', '.join(row)
            result.add_row(row)

    # print str(result).replace("  ", "")
    with open(args.output_md, 'w') as out:
        out.write(str(result).replace("  ", ""))


if __name__ == "__main__":
    #test()
    init_logger()
    # logging.info('Started')
    main()
    # logging.info('Finished')
