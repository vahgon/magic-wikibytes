from lib.exceptions import NoTagFoundError
import re

try:
    import bs4
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("bs4 not found. Install with -> pip install bs4")
    raise e

table_headers: list[str] = list()
table_rows: list[dict[str, str | None]] = list()

def is_empty(col: str | None) -> str | None:
    return None if col == '' else col

def set_headers(h_row: bs4.Tag) -> None:
    global table_headers
    table_headers = [x.get_text() for x in h_row.children]

def set_normal_row(row: bs4.Tag) -> None:
    global table_rows
    if not table_headers:
        set_headers(row.extract())
        return
    
    # substitutes in text citation (e.g. [23]) for empty string
    fsig_info = {key: is_empty(re.sub(r'( ?\[[0-9]*\])', '', val.text)) for key, val in zip(table_headers, row.find_all('td'))}
    table_rows.append(fsig_info)
    row.decompose()

def set_abnormal_row(row: bs4.Tag) -> None:
    for col in row.find_all('td'):
        col.decompose()

def format_parsed_table(table_body: bs4.Tag) -> None:
    for row in table_body.find_all('tr'):
        if len(row) == 5:
            set_normal_row(row)
        else:
            set_abnormal_row(row)

def parse_html(html: str) -> list[dict[str, str | None]]:
    table = bs4.BeautifulSoup(markup=html.replace('\n', ''), 
                              parse_only=bs4.filter.SoupStrainer('table', { 'class': 'wikitable sortable' }), 
                              features='lxml') 
    tbody = table.find('tbody', recursive=True)

    if not isinstance(tbody, bs4.Tag):
        e = NoTagFoundError()
        e.add_note("No tbody tag found in HTML.")
        raise e

    format_parsed_table(tbody)
    return table_rows
