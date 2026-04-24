#!/bin/env python

import asyncio
from sys import argv

from wikibytes.parser import Table
from wikibytes.util import parse_args


async def call_format_wikimedia(args: list[str]) -> None:
    await Table(parse_args(args))

def main(args: list[str]) -> None:
    asyncio.run(call_format_wikimedia(args))

def _main() -> None:
    main(argv[1:])

if __name__ == '__main__':
    _main()
