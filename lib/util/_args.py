from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys

def parse_args(u_args: list[str] = sys.argv[1:]) -> Namespace:
    parser = ArgumentParser(usage='python wikibytes.py [-v | -q] [-e email]', color=False, suggest_on_error=True,
                            description="""Parses and formats the table of file signatures
                            found at wikipedia's \"List_of_file_signatures\" page""")

    parser.add_argument('-e', '--email', required=False, type=str, metavar='', default=None,
                        help="""Specify the email address to be used in the user-agent header 
                        in requests made to the wikipedia API. you can read why this should be set
                        at \"https://en.wikipedia.org/wiki/Special:RestSandbox/wmf-restbase\".""")

    determine_output = parser.add_mutually_exclusive_group()

    determine_output.add_argument('-o', '--output', required=False, type=Path, metavar='', default=None, 
                                  help="""Specify the output file. if none specified, output will be printed 
                                  to console. default filetype is json if none is included.""")

    determine_output.add_argument('-f', '--format', required=False, type=str, metavar='', default=None, choices=['json','csv','md'],
                                  help="""Prints output to the terminal in the format specified by input given (e.g. -e json).""")

    determine_output.add_argument('-d', '--docs', required=False, action='store_true', 
                                  help="""Will create all supported filetypes & send to docs/""")

    parser.add_argument('--hex', required=False, type=str, metavar='', default=None, choices=['prefix'], help="""set hex output format.""")

    parser.add_argument('--rowspan-newrow', required=False, action='store_true',
                        help="""Succeeding rows affected by rowspan attributes in the current row's 
                        columns will have their own instances when parsed instead of being appended to
                        the current row.""")

    parser.add_argument('--little-endian', required=False, action='store_true',
                        help="""Output will not feature big-endian rows.""")

    terminal_vol = parser.add_mutually_exclusive_group()
    terminal_vol.add_argument('--verbose', required=False, action='store_true', help="""Print actions as they are taken during script execution.""")

    terminal_vol.add_argument('--quiet', required=False, default=False, action='store_true', help="""Supress all messages that would usually appear during %(prog)s's execution.""")

    return parser.parse_args(u_args)
