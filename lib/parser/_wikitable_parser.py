from lib.exceptions import NoTagFoundError
from lib.util import TableHeaders, TableRows
import re

try:
    import bs4
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("bs4 not found. Install with -> pip install bs4")
    raise e

tableHeaders: TableHeaders = list()
tableRows: TableRows = list()

def is_empty(col: str | None) -> str | None:
    return None if col == '' else col

def set_headers(h_row: bs4.Tag) -> None:
    global tableHeaders 
    tableHeaders = [x.get_text() for x in h_row.children]

def set_normal_row(row: bs4.Tag) -> None:
    global tableRows 
    if not tableHeaders:
        set_headers(row.extract())
        return
    
    # substitutes in text citation (e.g. [23]) for empty string
    fileSigInfo = {key: is_empty(re.sub(r'( ?\[[0-9]*\])', '', val.text)) for key, val in zip(tableHeaders, row.find_all('td'))}
    tableRows.append(fileSigInfo)
    row.decompose()

def set_abnormal_row(row: bs4.Tag) -> None:
    for col in row.find_all('td'):
        col.decompose()

def format_parsed_table(tableBody: bs4.Tag) -> None:
    for row in tableBody.find_all('tr'):
        if len(row) == 5:
            set_normal_row(row)
        else:
            set_abnormal_row(row)

def parse_html(html: str) -> list[dict[str, str | None]]:
    table = bs4.BeautifulSoup(markup=html.replace('\n', ''),
                              parse_only=bs4.filter.SoupStrainer('table', { 'class': 'wikitable sortable' }),
                              features='lxml')

    for br in table.find_all('br'):
        _ = br.replace_with('\n')

    tbody = table.find('tbody', recursive=True)
    if not isinstance(tbody, bs4.Tag):
        e = NoTagFoundError()
        e.add_note("No tbody tag found in HTML.")
        raise e

    format_parsed_table(tbody)
    return tableRows
