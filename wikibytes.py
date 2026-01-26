#!/bin/env python

from lib.parser import Table
import logging

def main() -> None:
    wiki_table: Table = Table()
    wiki_table.make_table()

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    try:
        main()
    except Exception as e:
        logging.exception(e)
