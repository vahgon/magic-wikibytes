from argparse import ArgumentParser, Namespace
import sys

class UserArgument:
    def __init__(self) -> None:
        args: Namespace = self.parse_args()

        self.email: str     =   args.email
        self.test: bool     =   args.test
        self.verbose: bool  =   args.verbose
        self.quiet: bool    =   args.quiet

    def parse_args(self, u_args: list[str] = sys.argv[1:]) -> Namespace:
        parser = ArgumentParser(usage='python wikibytes.py [-v | -q] [-e email]', color=False, suggest_on_error=True,
                                description="""parses and formats the table of file signatures
                                found at wikipedia's \"List_of_file_signatures\" page""")

        parser.add_argument('-e', '--email', required=False, type=str, metavar='', default=None,
                            help="""specify the email address to be used in the user-agent header 
                            in requests made to the wikipedia API. you can read why this should be set
                            at \"https://en.wikipedia.org/wiki/Special:RestSandbox/wmf-restbase\"""")

        parser.add_argument('-t', '--test', action='store_true',
                            help="""run all unit tests""")

        parser.add_argument('-v', '--verbose', required=False, action='store_true',
                            help="""print actions as they are taken during script execution""")

        parser.add_argument('-q', '--quiet', required=False, default=False, action='store_true',
                            help="""supress all messages that would usually appear
                            during script execution of %(prog)s""")

        return parser.parse_args(u_args)
