#!/bin/env python

import bs4
import re
import requests
import pathlib
import dotenv

env_path = f'{pathlib.Path(__file__).resolve().parent}/.env'
wikimedia_api_call = 'https://en.wikipedia.org/api/rest_v1/page/html/List_of_file_signatures'

class DotenvError(Exception):
    pass

class MissingContentError(Exception):
    pass

class ElementError(Exception):
    pass

class NoTagFound(Exception):
    pass

def set_header() -> dict[str, str]:
    if not pathlib.Path(env_path).exists():
        file = env_path
        with open(file, 'w') as f:

            set_usr_email = "EMAIL=" + input("Please provide an email address to use when making requests to the wikipedia API: ") 
            _ = f.write(set_usr_email)
            f.close()

    env_val = dotenv.dotenv_values(env_path)
    email = env_val['EMAIL'] if env_val['EMAIL'] is not None else ''

    if email != '': 
        return { 'User-Agent': email, 'Accept-Language': 'en' }
    else:
        raise DotenvError(f"'EMAIL' is not set in {env_path}")


def make_request():
    req = wikimedia_api_call
    header = set_header()

    res = requests.get(url=req, headers=header)
    res.raise_for_status()

    format_response(res)

def pop_row(rows: bs4.ResultSet[bs4.Tag]):
    rows[0].decompose
    _ = rows.pop(0)

is_hex          = re.compile(pattern=r'(([A-F0-9?]{2})+\s)+([A-F0-9]{2})$')
is_iso          = re.compile(pattern=r'')
is_offset       = re.compile(pattern=r'',                                       flags=re.IGNORECASE)
is_extension    = re.compile(pattern=r'',                                       flags=re.IGNORECASE)
is_desc         = re.compile(pattern=r'',                                       flags=re.IGNORECASE)
is_l_end_hex    = re.compile(pattern=r'little-endian(?!.*big-endian)',          flags=re.IGNORECASE)
is_b_end_hex    = re.compile(pattern=r'big-endian(?!.*little-endian)',          flags=re.IGNORECASE)

def find_content(data: bs4.Tag | None) -> str | None:
    if data is None:
        raise NoTagFound(f'No tag found for {data}')
    if data.is_empty_element:
        return

    if re.search(pattern=is_hex, string=data.get_text()):
        return 'hex'

def format_table(rows: bs4.ResultSet[bs4.Tag]) -> None:
    table: dict[str, str | None] = {}

    for header in rows[0]:
        table[header.get_text()] = None
    pop_row(rows)

    while True:
        if len(rows) >= 1:
            for col in rows[0]:
                match find_content(col.find_next()):
                    case 'hex':
                        print(col)
                    case None:
                        pass
                    case _:
                        raise ElementError(f'Default case for {col.get_text} (this shouldn\'t happen)')

            pop_row(rows)
        else:
            break

def format_response(res: requests.Response):
    from bs4.filter import SoupStrainer
    table = bs4.BeautifulSoup(markup=res.text.replace('\n', ''), parse_only=SoupStrainer('table',{ 'class': 'wikitable sortable' }), features='lxml')
    table_body = table.find('tbody', recursive=True)

    if not isinstance(table_body, bs4.Tag):
        raise NoTagFound('GET response did not return a table with a <tbody></tbody> tags')

    rows = table_body.find_all('tr')
    format_table(rows)

if __name__ == "__main__":
    res = make_request()
