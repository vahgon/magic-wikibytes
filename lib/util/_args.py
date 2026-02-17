from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys

def parse_args(u_args: list[str] = sys.argv[1:]) -> Namespace:
    parser = ArgumentParser(usage='python wikibytes.py [-v | -q] [-e email]', color=False, suggest_on_error=True,
                            description="""parses and formats the table of file signatures
                            found at wikipedia's \"List_of_file_signatures\" page""")

    _ = parser.add_argument('-e', '--email', required=False, type=str, metavar='', default=None,
                            help="""specify the email address to be used in the user-agent header 
                            in requests made to the wikipedia API. you can read why this should be set
                            at \"https://en.wikipedia.org/wiki/Special:RestSandbox/wmf-restbase\"""")

    determineOutput = parser.add_mutually_exclusive_group()

    _ = determineOutput.add_argument('-o', '--output', required=False, type=Path, metavar='', default=None,
                            help="""specify the output file. if none specified, output will be 
                            printed to console. default filetype is json if none is included.""")

    _ = determineOutput.add_argument('-f', '--format', required=False, type=str, metavar='', default=None, choices=['json','csv','md'],
                            help="""prints output to the terminal in the format specified by input
                            given (e.g. -e json)""")

    _ = determineOutput.add_argument('-d', '--docs', required=False, action='store_true',
                            help="""will create all supported filetypes & send to docs/""")

    _ = parser.add_argument('--hex', required=False, type=str, metavar='', default=None, choices=['prefix'],
                            help="""set hex output format""")

    terminalVolume = parser.add_mutually_exclusive_group()

    _ = terminalVolume.add_argument('-v', '--verbose', required=False, action='store_true',
                            help="""print actions as they are taken during script execution""")

    _ = terminalVolume.add_argument('-q', '--quiet', required=False, default=False, action='store_true',
                            help="""supress all messages that would usually appear
                            during %(prog)s's execution.""")

    return parser.parse_args(u_args)
