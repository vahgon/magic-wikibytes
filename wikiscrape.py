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

def format_response(res: Response):
    from bs4 import BeautifulSoup                                      # noqa: E402
    soup  = BeautifulSoup(markup=res.text, features='lxml')
    table = soup.select_one('table[class~=wikitable]')

    if table is None:
        raise MissingContentError(f"Request to '{wikimedia_api_call}' did not return a table of class 'wikitable'")

    rows = List[Row]

    for r in table.css.select('tr'):
        children = r.find_all()
        row: Row.columns = []
        for child in children:
            col: Column = { 'tag_name': str(type(child)), 'tag': child, 'content': child.text }
            row.append(col)

            #if child.name == 'code':
                #print(child)
            #elif child.name != 'th':
                #print(child)
                #pass

if __name__ == "__main__":
    res = make_request()
