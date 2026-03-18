import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class UserArguments:
    email:      (str | None)
    format:     (str | None)
    output:     str
    hexspacing: str
    wildcard:   str

    no_bigend:   bool = False
    span_newrow: bool = False
    noparen:     bool = False
    force_latin: bool = False
    verbose:     bool = False
    quiet:       bool = False

    @classmethod
    def usr_args(cls, args) -> "UserArguments":
        return cls(
            email       = args.email,
            output      = args.output,
            format      = args.format,
            hexspacing  = args.hex_separator,
            wildcard    = args.wildcard_char,
            span_newrow = args.rowspan_newrow,
            noparen     = args.ext_parens,
            no_bigend   = args.no_bigend,
            force_latin = args.force_latin1,
            verbose     = args.verbose,
            quiet       = args.quiet
        )

def parse_args(u_args: list[str] = sys.argv[1:]) -> UserArguments:
    parser = ArgumentParser(usage='python wikibytes.py [-v | -q] [-e email]', color=False, suggest_on_error=True,
                            description="""Parses and formats the table of file signatures
                            found at wikipedia's \"List_of_file_signatures\" page""")

    parser.add_argument('-e', '--email', required=False, type=str, metavar='', default=None,
                        help="""Specify the email address to be used in the user-agent header
                        in requests made to the wikipedia API. you can read why this should be set
                        at \"https://en.wikipedia.org/wiki/Special:RestSandbox/wmf-restbase\".""")

    parser.add_argument('-o', '--output', required=False, type=str, metavar='', default='.',
                        help="""Specify the output file. if none specified, output will be printed
                        to console. default filetype is json if none is included.""")

    parser.add_argument('-f', '--format', required=False, type=str, metavar='', default=None, choices=['json', 'md', 'all'],
                        help="""Prints output to the terminal in the format specified by input given (e.g. -e json).""")

    parser.add_argument('--hex-separator', required=False, type=str, metavar='', default='',
                        help="""Specify character/string to use to separate hexadecimal bytes (default = '').""")

    parser.add_argument('--wildcard-char', required=False, type=str, metavar='', default='?',
                        help="""Specify a character to act as found wildcard bytes (default='?')""")

    parser.add_argument('--rowspan-newrow', required=False, action='store_true',
                        help="""Succeeding rows affected by rowspan attributes in the current row's
                        columns will have their own instances when parsed instead of being appended to
                        the current row.""")

    parser.add_argument('--ext-parens', required=False, action='store_true',
                        help="""Remove parenthesis found in file signature extension(s).""")

    parser.add_argument('--no-bigend', required=False, action='store_true',
                        help="""Ignore all big-endian formatted rows from the wikitable.""")

    parser.add_argument('--force-latin1', required=False, action='store_true',
                        help="""Force the decoding of all hexadecimal values to latin-1 instead of
                        only unbalanced iso-8559 and hexadecimal columns.""")

    terminal_vol = parser.add_mutually_exclusive_group()

    terminal_vol.add_argument('--verbose', required=False, action='store_true',
                        help="""Print actions as they are taken during script execution.""")

    terminal_vol.add_argument('--quiet', required=False, default=False, action='store_true',
                        help="""Supress all messages that would usually appear during %(prog)s's execution.""")

    return UserArguments.usr_args(parser.parse_args(u_args))
