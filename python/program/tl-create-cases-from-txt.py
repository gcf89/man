#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Преобразователь кастомного формата кейсов для TestLink в родной xml
"""


import argparse
import logging
import logging.config


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
            # 'file': {
            #     'level': 'DEBUG',
            #     'class': 'logging.FileHandler',
            #     'formatter': 'default',
            #     'filename': 'out1.log',
            #     # 'mode': 'w',
            #     # 'encoding': 'utf-8',
            # },
        },
        'root': {
            'level': 'DEBUG',
            # 'handlers': ['console', 'file']
            'handlers': ['console']
        },
    }

    logging.config.dictConfig(loggin_config)


def test():
    """
    Simple docsting test
    """
    import doctest
    doctest.testmod()


def insert_header(name, fout):
    data="""<?xml version="1.0" encoding="UTF-8"?>

    <testsuite name="{0}" >
    <node_order><![CDATA[1]]></node_order>
    <details><![CDATA[]]></details>

    """.format(name)

    fout.write(data)


def insert_footer(fout):
    data="""
    </testsuite>
    """
    fout.write(data)


def insert_case_header(name, summary, precond, fout):
    data="""
    <testcase name="{0}">
    <node_order><![CDATA[0]]></node_order>
    <version><![CDATA[2]]></version>

    <summary><![CDATA[
    {1}
    ]]></summary>

    <preconditions><![CDATA[
    {2}
    ]]></preconditions>

    <execution_type><![CDATA[1]]></execution_type>
    <importance><![CDATA[2]]></importance>
    <estimated_exec_duration></estimated_exec_duration>
    <status>1</status>
    <is_open>1</is_open>
    <active>1</active>

    <steps>
    """.format(name, summary, precond)

    fout.write(data)


def insert_case_footer(fout):
    data="""
    </steps>
    </testcase>
    """

    fout.write(data)


def insert_case_step(step_num, actions, expected_results, fout):
    data="""
    <step>
    <step_number><![CDATA[{0}]]></step_number>

    <actions><![CDATA[
    {1}
    ]]></actions>

    <expectedresults><![CDATA[
    {2}
    ]]></expectedresults>

    <execution_type><![CDATA[1]]></execution_type>
    </step>
    """.format()

    fout.write(data)



def main():
    """
    Start point
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input_file", default="",
                        help="Input file")
    parser.add_argument("-o", "--output", dest="output_file", default="",
                        help="Output file")
    args = parser.parse_args()

    with open(args.input_file) as fin:
        with open(args.output_file, 'w') as fout:
            insert_header('test1', fout)
            for line in reversed(list(fin)):
                insert_case_header(line.rstrip(), '', '', fout)
                insert_case_footer(fout)
            insert_footer(fout)


if __name__ == "__main__":
    # test()
    init_logger()
    logging.info('Started')
    main()
    logging.info('Finished')
