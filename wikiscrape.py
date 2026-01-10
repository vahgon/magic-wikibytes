#!/bin/env python


from dotenv import dotenv_values
from pathlib import Path

from urllib3.util import url

env_path = f'{Path(__file__).resolve().parent}/.env'
wikimedia_api_call = 'https://en.wikipedia.org/api/rest_v1/page/html/List_of_file_signatures'

class DotenvError(Exception):
    pass

class MissingContentError(Exception):
    pass

def set_header() -> dict[str, str]:
    if not Path(env_path).exists():
        file = env_path
        with open(file, 'w') as f:

            set_usr_email = "EMAIL=" + input("Please provide an email address to use when making requests to the wikipedia API: ") 
            _ = f.write(set_usr_email)
            f.close()

    env_val = dotenv_values(env_path)
    email = env_val['EMAIL'] if env_val['EMAIL'] is not None else ''

    if email != '': 
        return { 'User-Agent': email, 'Accept-Language': 'en' }
    else:
        raise DotenvError(f"'EMAIL' is not set in {env_path}")

from requests import Response  # noqa: E402
def make_request():
    req = wikimedia_api_call
    header = set_header()

    from requests import get
    res = get(url=req, headers=header)  
    res.raise_for_status()

    format_response(res)

import bs4  # noqa: E402
def format_response(res: Response):
    soup  = bs4.BeautifulSoup(markup=res.text, features='lxml')

    table = soup.select_one('table[class~=wikitable]')
    if table is None:
        raise MissingContentError(f"Request to '{url}' did not return a table of class 'wikitable'")

    rows: list[bs4.Tag] = []
    for row in table.css.select('tr'):
        children = row.find_all()
        for child in children:
            if child.name == 'th':
                print(child)
            elif child.name != 'th':
                print(child)


        #rows.append(row)

    #headers: list[bs4.Tag] = []
    # for header in rows.index(value=, start=0, end=sys.maxsize):


        

if __name__ == "__main__":
    res = make_request()
