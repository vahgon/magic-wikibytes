#!/bin/env python

from lib.parser import Table
from lib.util import log

def main() -> None:
    wiki_table: Table = Table()
    wiki_table.make_table()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log.exception(e)
