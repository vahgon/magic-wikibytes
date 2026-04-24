from argparse import ArgumentParser, Namespace
from pathlib import Path


def parse_args(args: list[str]) -> Namespace:
    parser          = ArgumentParser(prog="wikibytes.py", color=False, suggest_on_error=True)

    table           = parser.add_argument_group("Table Format Options")
    hex_fmt         = parser.add_argument_group("Hex Format Options")
    terminal_vol    = parser.add_mutually_exclusive_group()

    parser.add_argument('-e', '--email', type=str, metavar='STR', dest='email',
                        help="""Specify the email address to be used in the user-agent header
                        in requests made to the wikipedia API. You can read why this should be set
                        at \"https://en.wikipedia.org/wiki/Special:RestSandbox/wmf-restbase\".""")

    parser.add_argument('-o', '--output', type=Path, metavar='PATH', dest='output',
                        help="""Specify the output file. if none specified, output will be printed
                        to console. default filetype is json if none is included.""")

    parser.add_argument('-f', '--force', required=False, action='store_true', dest='force',
                        help="Force create the table by skipping revision id comparison.")

    hex_fmt.add_argument('--hex-separator', type=str, metavar='STR', default='', dest='hexsep_char',
                         help="Specify character/string to use to separate hexadecimal bytes")

    hex_fmt.add_argument('--wildcard-char', type=str, metavar='CHAR', default='?', dest='wildcard_char',
                         help="Specify a character to act as found wildcard bytes (default='?')")

    #  Table format options
    table.add_argument('--rowspan-newrow', required=False, action='store_true', dest='newrow_cr',
                       help="""Succeeding rows affected by rowspan attributes in the current row's
                       columns will have their own instances when parsed instead of being appended to
                       the current row.""")

    table.add_argument('--ext-parens', required=False, action='store_true', dest='ext_paren',
                       help="Remove parenthesis found in file signature extension(s).")

    table.add_argument('--no-big-end', required=False, action='store_true', dest='no_bigend',
                       help="Ignore all big-endian formatted rows from the wikitable.")

    table.add_argument('--force-latin1', required=False, action='store_true', dest='force_latin',
                       help="""Force the decoding of all hexadecimal values to latin-1
                       instead of only unbalanced iso-8559 and hexadecimal columns.""")

    terminal_vol.add_argument('--verbose', required=False, action='store_true', dest='verbose',
                              help="""Print actions as they are taken during script execution.""")

    terminal_vol.add_argument('--quiet', required=False, default=False, action='store_true', dest='quiet',
                              help="Supress messages that would usually appear during %(prog)s's execution.")

    return parser.parse_args(args)
